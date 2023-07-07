import cocotb
from cocotb.triggers import RisingEdge, Timer, Combine, Edge, FallingEdge

from uvm.base.sv import sv_if, sv

class clk_rst_if(sv_if):
    def __init__(self, dut, bus_name, clk_name, rst_name):
        bus_map = {}
        bus_map["clk"] = clk_name
        bus_map["rst"] = rst_name
        # bus_map = {"sig_reset": "reset", "sig_clock": "clock", "sig_size":
        #         "size", "sig_read": "read", "sig_write": "write",
        #         "sig_bip": "bip", "sig_start": "start", "sig_addr": "addr",
        #         "sig_data": "data", "sig_data_out": "data",
        #         "sig_error": "error", "sig_wait": "wait",
        #         "sig_request": "req_master_0",
        #         "sig_grant": "gnt_master_0"}
        sv_if.__init__(self, dut, bus_name, bus_map)
        self.clk = self._signals["clk"]
        self.rst = self._signals["rst"]
        self.rst_assert_val = None
        self.run_clock = False
        self.clk_period_ns = 100 # default time period is 100ns
        # Control flags
        self.has_checks = True
        self.has_coverage = True

    # deposit initial value to clock
    def init(self, clk_val = 0, rst_val = 0):
        self.clk.value = clk_val
        self.rst.value = rst_val
        self.rst_assert_val = rst_val

    async def start_clock(self):
        self.run_clock = True
        print("CLK started")
        while self.run_clock:
            self.clk.value = 0
            await Timer(self.clk_period_ns/2, "NS")
            self.clk.value = 1
            await Timer(self.clk_period_ns/2, "NS")

    def stop_clock(self):
        self.run_clock = False

    def set_clk_period_ns(self, clk_period_ns):
        self.clk_period_ns = clk_period_ns

    # Assert reset for a given number of cycles
    async def assert_reset(self, cycles = 10):
        self.rst.value = self.rst_assert_val
        for i in range(cycles):
            await RisingEdge(self.clk)
        self.rst.value = ~self.rst_assert_val
            

