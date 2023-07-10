# Licensed under the Apache License, Version 2.0, see LICENSE for details.
# SPDX-License-Identifier: Apache-2.0
# Author : Raviteja Chatta

from uvm.base.uvm_config_db import UVMConfigDb
from uvm.base.uvm_component import UVMComponent, UVMObject
from uvm.macros import uvm_component_utils 
from uvm.macros.uvm_global_defines import UVM_HIGH
from dv.agent.dv_lib.dv_base_agent_cfg import dv_base_agent_cfg
from dv.agent.common import if_mode_e

@uvm_component_utils
class dv_base_agent(UVMComponent):
    def __init__(self, name, parent):
        super().__init__(name, parent)
        self.cfg : dv_base_agent_cfg= None
        self.cov : UVMObject = None
        self.driver : UVMComponent = None
        self.sequencer : UVMComponent = None
        self.monitor : UVMComponent = None
    
    def build_phase(self, phase):
        super().build_phase(phase)
        if UVMConfigDb.get(self, "", "cfg", self.cfg) is False:
            self.uvm_report_fatal(self.get_full_name(), "No configuration object found for ")
        else:
            self.uvm_report_info(self.get_full_name(), "Configuration object found for " + self.cfg.get_full_name(), UVM_HIGH)
        if self.cfg.en_cov:
            self.cov = self.cov.type_id.create("cov", self)
            self.cov.cfg = self.cfg
        
        # Create monitor component
        self.monitor = self.cfg.monitor.type_id.create("monitor", self)
        self.monitor.cfg = self.cfg
        self.monitor.cov = self.cov

        # Create sequencer based on configuration input
        if self.cfg.is_active:
            self.sequencer = self.sequencer.type_id.create("sequencer", self)
            self.sequencer.cfg = self.cfg
            if self.cfg.has_driver:
                self.driver = self.driver.type_id.create("driver", self)
                self.driver.cfg = self.cfg
                
    def connect_phase(self, phase):
        super().connect_phase(phase)
        if self.cfg.is_active and self.cfg.has_driver:
            self.driver.seq_item_port.connect(self.sequencer.seq_item_export)
        if self.cfg.has_req_fifo:
            self.monitor.req_fifo.connect(self.sequencer.req_analysis_fifo.analysis_export)
        if self.cfg.has_rsp_fifo:
            self.sequencer.rsp_export.connect(self.sequencer.rsp_analysis_fifo.analysis_export)

