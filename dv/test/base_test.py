import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Timer

from uvm import *

# from tb_env import tb_env

# Set to True to allow VIPs (drivers/monitors) raise/drop objections
#hier_objection = False


class base_test(UVMTest):

    def __init__(self, name, parent=None):
        super().__init__(name, parent)
        #self.env = tb_env("env")
        #self.env.hier_objection = hier_objection


    def start_of_simulation_phase(self, phase):
        cs_ = UVMCoreService.get()
        top = cs_.get_root()

    def check_phase(self, phase):
        self.error = self.env.has_errors()
        if self.error:
            uvm_fatal("TEST FAILED", "check_phase of test threw fatal")


uvm_component_utils(base_test)


async def do_reset_and_start_clocks(dut):
    dut.clk_i <= 0
    await Timer(100, "NS")
    dut.rst_ni <= 0
    await Timer(200, "NS")
    dut.rst_ni <= 1
    dut.clk_i <= 0
    await Timer(500, "NS")
    cocotb.start_soon(Clock(dut.clk, 50, "NS").start())


@cocotb.test()
async def test_codec(dut):

    # UVMConfigDb.set(None, "env", "vif", ctl)
    # UVMConfigDb.set(None, "env.apb", "vif", apb_vif)
    # UVMConfigDb.set(None, "env.vip", "vif", vip0)

    cocotb.start_soon(do_reset_and_start_clocks(dut))

    await run_test()
