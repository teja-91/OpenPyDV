# Licensed under the Apache License, Version 2.0, see LICENSE for details.
# SPDX-License-Identifier: Apache-2.0
# Author : Raviteja Chatta
from uvm.base.uvm_object import UVMObject
from dv.agent.common import if_mode_e
from uvm.macros.uvm_object_defines import *
from uvm.base.uvm_object_globals import *

class dv_base_agent_cfg(UVMObject):
  def __init__(self, name = "dv_base_agent_cfg"):
    super().__init__(name)
    # active driver/sequencer or passive monitor
    self.is_active = 1
    # enable coverage
    self.en_cov = 1
    # interface mode - Host or Device
    self.if_mode = if_mode_e.HOST
    # indicate to create and connet driver to sequencer or not
    # if this is a high-level agent, we may just call lower-level agent to send item in seq, then
    #  driver isn't needed
    self.has_driver = 1
    # indicate if these fifo and ports exist or not
    self.has_req_fifo = 0
    self.has_rsp_fifo = 0
    # use for phase_ready_to_end to add additional delay after ok_to_end is set
    self.ok_to_end_delay_ns = 1000
    # Indicates that the interface is under reset. The derived monitor detects and maintains it.
    self.in_reset = 0
    # Indicates if Monitor is enabled or not
    self.en_monitor = 1
    # UVM automation macros for general objects
    uvm_object_utils_begin(dv_base_agent_cfg)
    uvm_field_int ("is_active",    UVM_DEFAULT)
    uvm_field_int ("en_cov",       UVM_DEFAULT)
    uvm_field_int("if_mode",       UVM_DEFAULT)
    uvm_field_int ("has_req_fifo", UVM_DEFAULT)
    uvm_field_int ("has_rsp_fifo", UVM_DEFAULT)
    uvm_object_utils_end
