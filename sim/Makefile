# Generic Simulation Makefile
# Works with ANY RTL design — just drop .sv files into rtl/ and tb/
# Author: Sindhu Govindareddy Doddamane

SIM_DIR  = ../sim
RTL_DIR  = ../rtl
TB_DIR   = ../tb

# Auto-detect ALL .sv files in rtl/ and tb/
RTL_FILES = $(wildcard $(RTL_DIR)/*.sv)
TB_FILES  = $(wildcard $(TB_DIR)/*.sv)

# Auto-detect design name from RTL folder
DESIGN_NAME = $(notdir $(basename $(firstword $(RTL_FILES))))
SIM_OUT     = $(SIM_DIR)/$(DESIGN_NAME)_sim

# Default target
all: check compile simulate coverage

# Check files exist
check:
	@echo "============================================"
	@echo "  DV Regression Pipeline"
	@echo "============================================"
	@echo "RTL  Files : $(RTL_FILES)"
	@echo "TB   Files : $(TB_FILES)"
	@echo "Design     : $(DESIGN_NAME)"
	@echo "============================================"

# Compile
compile:
	@echo "Compiling design: $(DESIGN_NAME)..."
	iverilog -g2012 -o $(SIM_OUT) $(RTL_FILES) $(TB_FILES)
	@echo "Compilation DONE ✅"

# Simulate
simulate:
	@echo "Running Simulation..."
	vvp $(SIM_OUT) | tee $(SIM_DIR)/sim_results.log
	@echo "Simulation DONE ✅"

# Coverage
coverage:
	@echo "Parsing Coverage..."
	python3 ../coverage/parse_coverage.py \
		$(SIM_DIR)/sim_results.log \
		$(DESIGN_NAME)
	@echo "Coverage DONE ✅"

# Clean
clean:
	@echo "Cleaning up..."
	rm -f $(SIM_DIR)/*_sim
	rm -f $(SIM_DIR)/*.vcd
	rm -f $(SIM_DIR)/*.log
	rm -f $(SIM_DIR)/*.json
	@echo "Clean DONE ✅"
