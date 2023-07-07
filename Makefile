# Copyright lowRISC contributors.
# Licensed under the Apache License, Version 2.0, see LICENSE for details.
# SPDX-License-Identifier: Apache-2.0

# Makefile for testing python-uvm

# Usage:
# To execute tests in given file using given verilog source, you can do:
# >$ make MODULE=py_mod_name VLOG=hdl/my_vlog.v SIM_ARGS='-aaa +bbb'
#

include $(PROJ_ROOT)/src/filelist.mk
TOPLEVEL_LANG ?= verilog
SIM ?= xcelium

PWD=$(shell pwd)
# add UVM path and test path
PYTHONPATH := $(PROJ_ROOT)/dv/test:$(PYTHONPATH)
PYTHONPATH += $(PROJ_ROOT)/uvm-python/src/uvm::$(PYTHONPATH)

export PYTHONPATH


PLUSARGS=+UVM_CONFIG_DB_TRACE=1 +UVM_VERBOSITY=UVM_MEDIUM
ifneq ($(UVM_TEST),)
    PLUSARGS += +UVM_TESTNAME=$(UVM_TEST)
endif

ifneq ($(SIMARGS),)
    PLUSARGS += $(SIMARGS)
endif

TOPLEVEL := i2c
MODULE   ?= base_test

print_path: 
	echo $(PYTHONPATH)

# Will be passed to compilation
#EXTRA_ARGS=""

include $(shell cocotb-config --makefiles)/Makefile.sim
