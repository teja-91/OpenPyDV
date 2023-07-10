# Licensed under the Apache License, Version 2.0, see LICENSE for details.
# SPDX-License-Identifier: Apache-2.0
# Author : Raviteja Chatta

from uvm.base.uvm_config_db import UVMConfigDb
from uvm.base.uvm_component import UVMComponent, UVMObject
from uvm.macros import uvm_component_utils 
from uvm.macros.uvm_global_defines import UVM_HIGH
from dv.agent.dv_lib.dv_base_agent_cfg import dv_base_agent_cfg
from cocotb import start_soon

@uvm_component_utils
class dv_base_agent(UVMComponent):
    def __init__(self, name, parent):
        super().__init__(name, parent)
        self.under_reset = None
        self.cfg : dv_base_agent_cfg= None

    async def run_phase(self, phase):
        await start_soon(self.reset_signals())
        await start_soon(self.get_and_driver())
    
    def reset_signals(self):
        self.uvm_report_fatal(self.get_full_name(), "This task must be extended")

    def get_and_driver(self):
        self.uvm_report_fatal(self.get_full_name(), "This task must be extended")
