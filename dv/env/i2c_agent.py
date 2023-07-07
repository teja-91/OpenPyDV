from uvm.base import *
from uvm.comps import UVMAgent
from uvm.macros import uvm_component_utils

#//------------------------------------------------------------------------------
#//
#// CLASS: i2c_agent
#//
#//------------------------------------------------------------------------------

@uvm_component_utils
class i2c_agent(UVMAgent):
    #  // new - constructor
    def __init__(self, name, parent):
        super().__init__(name, parent)

    def build_phase(self, phase):
        super().build_phase(phase)

