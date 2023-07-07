import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Timer

from uvm import *
from env.i2c_env import i2c_env

# from tb_env import tb_env

# Set to True to allow VIPs (drivers/monitors) raise/drop objections
#hier_objection = False


class base_test(UVMTest):

    def __init__(self, name, parent=None):
        super().__init__(name, parent)
        self.env = None
        #self.env.hier_objection = hier_objection

    def build_phase(self, phase):
        super().build_phase(phase)
        self.env = i2c_env.type_id.create("i2c_env", self)

    def start_of_simulation_phase(self, phase):
        cs_ = UVMCoreService.get()
        top = cs_.get_root()

    async def run_phase(self, phase):
        super().run_phase(phase)
        phase.raise_objection(self, "base_test_start")
        cs_ = UVMCoreService.get()
        self.top = cs_.get_root()
        self.top.print_topology()
        # get dut handle
        dut = None
        UVMConfigDb.set(self, "*", "dut", dut)
        await Timer(2000, "NS")
        phase.drop_objection(self, "base_test_end")
        

    # def check_phase(self, phase):
    #     self.error = self.env.has_errors()
    #     if self.error:
    #         uvm_fatal("TEST FAILED", "check_phase of test threw fatal")


uvm_component_utils(base_test)


async def do_reset_and_start_clocks(dut):
    clk_i = 0
    await Timer(100, "NS")
    rst_ni = 0
    await Timer(200, "NS")
    rst_ni = 1
    clk_i = 0
    await Timer(500, "NS")
    cocotb.start_soon(Clock(dut.clk_i, 50, "NS").start())


@cocotb.test()
async def test_i2c_basic_clock_and_reset(dut):

    # UVMConfigDb.set(None, "env", "vif", ctl)
    # UVMConfigDb.set(None, "env.apb", "vif", apb_vif)
    # UVMConfigDb.set(None, "env.vip", "vif", vip0)

    cocotb.start_soon(do_reset_and_start_clocks(dut))
    UVMConfigDb.set(None, "*", "dut", dut)

    await run_test("base_test")
