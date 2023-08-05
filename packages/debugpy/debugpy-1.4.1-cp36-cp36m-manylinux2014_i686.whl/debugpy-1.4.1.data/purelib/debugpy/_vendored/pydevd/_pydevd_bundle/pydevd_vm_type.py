import sys

#=======================================================================================================================
# PydevdVmType
#=======================================================================================================================
class PydevdVmType:
    
    PYTHON = 'python'
    JYTHON = 'jython'
    vm_type = None

    
#=======================================================================================================================
# set_vm_type
#=======================================================================================================================
def set_vm_type(vm_type):
    PydevdVmType.vm_type = vm_type
    
    
#=======================================================================================================================
# get_vm_type
#=======================================================================================================================
def get_vm_type():
    if PydevdVmType.vm_type is None:
        setup_type()
    return PydevdVmType.vm_type


#=======================================================================================================================
# setup_type
#=======================================================================================================================
def setup_type(str=None):
    if str is not None:
        PydevdVmType.vm_type = str
        return
    
    if sys.platform.startswith("java"):
        PydevdVmType.vm_type = PydevdVmType.JYTHON
    else:
        PydevdVmType.vm_type = PydevdVmType.PYTHON
        
