import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Timer

from uvm import *
from env.i2c_env import i2c_env
from env.clk_rst_if import clk_rst_if


@uvm_component_utils
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
        clk_rst_if = []
        # get dut handle
        if UVMConfigDb.get(self, "*", "clk_rst_if", clk_rst_if):
          UVMConfigDb.get(self, "*", "clk_rst_if", clk_rst_if)
        else:
          uvm_error(self.get_name(), "clk_rst_if not set in test top")
        clk_rst_if[0].clk_period_ns = 20;
        cocotb.start_soon(clk_rst_if[0].start_clock())
        await clk_rst_if[0].assert_reset(20)
        await Timer(2000, "NS")
        phase.drop_objection(self, "base_test_end")
        

@cocotb.test()
async def test_i2c_basic_clock_and_reset(dut):

    # Set clk_rst_if in UVM Config DB
    i2c_clk_rst_if = clk_rst_if(dut, "", "clk_i", "rst_ni")
    i2c_clk_rst_if.init()

    # cocotb.start_soon(do_reset_and_start_clocks(dut))
    UVMConfigDb.set(None, "*", "clk_rst_if", i2c_clk_rst_if)

    await run_test("base_test")
