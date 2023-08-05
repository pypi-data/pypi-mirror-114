from collections import namedtuple
import dis
from functools import partial
import itertools
import os.path

from _pydevd_frame_eval.vendored import bytecode
from _pydevd_frame_eval.vendored.bytecode.instr import Instr, Label
from _pydev_bundle import pydev_log
from _pydevd_frame_eval.pydevd_frame_tracing import _pydev_stop_at_break, _pydev_needs_stop_at_break

DEBUG = False


class DebugHelper(object):

    def __init__(self):
        self._debug_dir = os.path.join(os.path.dirname(__file__), 'debug_info')
        try:
            os.makedirs(self._debug_dir)
        except:
            pass
        self._next = partial(next, itertools.count(0))

    def _get_filename(self, op_number=None, prefix=''):
        if op_number is None:
            op_number = self._next()
            name = '%03d_before.txt' % op_number
        else:
            name = '%03d_change.txt' % op_number

        filename = os.path.join(self._debug_dir, prefix + name)
        return filename, op_number

    def write_bytecode(self, b, op_number=None, prefix=''):
        filename, op_number = self._get_filename(op_number, prefix)
        with open(filename, 'w') as stream:
            bytecode.dump_bytecode(b, stream=stream, lineno=True)
        return op_number

    def write_dis(self, code_to_modify, op_number=None, prefix=''):
        filename, op_number = self._get_filename(op_number, prefix)
        with open(filename, 'w') as stream:
            stream.write('-------- ')
            stream.write('-------- ')
            stream.write('id(code_to_modify): %s' % id(code_to_modify))
            stream.write('\n\n')
            dis.dis(code_to_modify, file=stream)
        return op_number


_CodeLineInfo = namedtuple('_CodeLineInfo', 'line_to_offset, first_line, last_line')


# Note: this method has a version in cython too (that one is usually used, this is just for tests).
def _get_code_line_info(code_obj):
    line_to_offset = {}
    first_line = None
    last_line = None

    for offset, line in dis.findlinestarts(code_obj):
        line_to_offset[line] = offset

    if line_to_offset:
        first_line = min(line_to_offset)
        last_line = max(line_to_offset)
    return _CodeLineInfo(line_to_offset, first_line, last_line)


if DEBUG:
    debug_helper = DebugHelper()


def get_instructions_to_add(
        stop_at_line,
        _pydev_stop_at_break=_pydev_stop_at_break,
        _pydev_needs_stop_at_break=_pydev_needs_stop_at_break
    ):
    '''
    This is the bytecode for something as:

        if _pydev_needs_stop_at_break():
            _pydev_stop_at_break()

    but with some special handling for lines.
    '''
    # Good reference to how things work regarding line numbers and jumps:
    # https://github.com/python/cpython/blob/3.6/Objects/lnotab_notes.txt
    label = Label()
    return [
        # -- if _pydev_needs_stop_at_break():
        Instr("LOAD_CONST", _pydev_needs_stop_at_break, lineno=stop_at_line),
        Instr("LOAD_CONST", stop_at_line, lineno=stop_at_line),
        Instr("CALL_FUNCTION", 1, lineno=stop_at_line),
        Instr("POP_JUMP_IF_FALSE", label, lineno=stop_at_line),

        #     -- _pydev_stop_at_break()
        #
        # Note that this has line numbers -1 so that when the NOP just below
        # is executed we have a spurious line event.
        Instr("LOAD_CONST", _pydev_stop_at_break, lineno=stop_at_line - 1),
        Instr("LOAD_CONST", stop_at_line, lineno=stop_at_line - 1),
        Instr("CALL_FUNCTION", 1, lineno=stop_at_line - 1),
        Instr("POP_TOP", lineno=stop_at_line - 1),

        # Reason for the NOP: Python will give us a 'line' trace event whenever we forward jump to
        # the first instruction of a line, so, in the case where we haven't added a programmatic
        # breakpoint (either because we didn't hit a breakpoint anymore or because it was already
        # tracing), we don't want the spurious line event due to the line change, so, we make a jump
        # to the instruction right after the NOP so that the spurious line event is NOT generated in
        # this case (otherwise we'd have a line event even if the line didn't change).
        Instr("NOP", lineno=stop_at_line),
        label,
    ]


class _Node(object):

    def __init__(self, data):
        self.prev = None
        self.next = None
        self.data = data

    def append(self, data):
        node = _Node(data)

        curr_next = self.next

        node.next = self.next
        node.prev = self
        self.next = node

        if curr_next is not None:
            curr_next.prev = node

        return node

    def prepend(self, data):
        node = _Node(data)

        curr_prev = self.prev

        node.prev = self.prev
        node.next = self
        self.prev = node

        if curr_prev is not None:
            curr_prev.next = node

        return node


class _HelperBytecodeList(object):
    '''
    A helper double-linked list to make the manipulation a bit easier (so that we don't need
    to keep track of indices that change) and performant (because adding multiple items to
    the middle of a regular list isn't ideal).
    '''

    def __init__(self, lst=None):
        self._head = None
        self._tail = None
        if lst:
            node = self
            for item in lst:
                node = node.append(item)

    def append(self, data):
        if self._tail is None:
            node = _Node(data)
            self._head = self._tail = node
            return node
        else:
            node = self._tail = self.tail.append(data)
            return node

    @property
    def head(self):
        node = self._head
        # Manipulating the node directly may make it unsynchronized.
        while node.prev:
            self._head = node = node.prev
        return node

    @property
    def tail(self):
        node = self._tail
        # Manipulating the node directly may make it unsynchronized.
        while node.next:
            self._tail = node = node.next
        return node

    def __iter__(self):
        node = self.head

        while node:
            yield node.data
            node = node.next


def insert_pydevd_breaks(
        code_to_modify,
        breakpoint_lines,
        code_line_info=None,
        _pydev_stop_at_break=_pydev_stop_at_break,
        _pydev_needs_stop_at_break=_pydev_needs_stop_at_break,
    ):
    """
    Inserts pydevd programmatic breaks into the code (at the given lines).

    :param breakpoint_lines: set with the lines where we should add breakpoints.
    :return: tuple(boolean flag whether insertion was successful, modified code).
    """
    if code_line_info is None:
        code_line_info = _get_code_line_info(code_to_modify)

    if not code_line_info.line_to_offset:
        return False, code_to_modify

    # Create a copy (and make sure we're dealing with a set).
    breakpoint_lines = set(breakpoint_lines)

    # Note that we can even generate breakpoints on the first line of code
    # now, since we generate a spurious line event -- it may be a bit pointless
    # as we'll stop in the first line and we don't currently stop the tracing after the
    # user resumes, but in the future, if we do that, this would be a nice
    # improvement.
    # if code_to_modify.co_firstlineno in breakpoint_lines:
    #     return False, code_to_modify

    try:
        b = bytecode.Bytecode.from_code(code_to_modify)

        if DEBUG:
            op_number_bytecode = debug_helper.write_bytecode(b, prefix='bytecode.')

        helper_list = _HelperBytecodeList(b)

        modified_breakpoint_lines = breakpoint_lines.copy()

        curr_node = helper_list.head
        while curr_node is not None:
            instruction = curr_node.data
            instruction_lineno = getattr(instruction, 'lineno', None)

            if instruction_lineno is not None:

                if instruction_lineno in modified_breakpoint_lines:
                    modified_breakpoint_lines.discard(instruction_lineno)
                    if curr_node.prev is not None and curr_node.prev.data.__class__ == Label \
                            and getattr(curr_node.data, 'name', None) == 'POP_TOP':

                        # If we have a SETUP_FINALLY where the target is a POP_TOP, we can't change
                        # the target to be the breakpoint instruction (this can crash the interpreter).

                        for new_instruction in get_instructions_to_add(
                            instruction_lineno,
                            _pydev_stop_at_break=_pydev_stop_at_break,
                            _pydev_needs_stop_at_break=_pydev_needs_stop_at_break,
                            ):
                            curr_node = curr_node.append(new_instruction)

                    else:
                        for new_instruction in get_instructions_to_add(
                            instruction_lineno,
                            _pydev_stop_at_break=_pydev_stop_at_break,
                            _pydev_needs_stop_at_break=_pydev_needs_stop_at_break,
                            ):
                            curr_node.prepend(new_instruction)

            curr_node = curr_node.next

        b[:] = helper_list

        if DEBUG:
            debug_helper.write_bytecode(b, op_number_bytecode, prefix='bytecode.')

        new_code = b.to_code()

    except:
        pydev_log.exception('Error inserting pydevd breaks.')
        return False, code_to_modify

    if DEBUG:
        op_number = debug_helper.write_dis(code_to_modify)
        debug_helper.write_dis(new_code, op_number)

    return True, new_code

