from uvm.base import *
from uvm.comps import UVMEnv
from uvm.macros import uvm_component_utils

from env.i2c_agent import i2c_agent

@uvm_component_utils
class i2c_env(UVMEnv):
	def __init__(self,name,parent):
		super().__init__(name, parent)
		self.agent = None

	def build_phase(self, phase):
		super().build_phase(phase)
		self.agent = i2c_agent.type_id.create("i2_agent", self)

