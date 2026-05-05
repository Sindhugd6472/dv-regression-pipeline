# Simulation Makefile
# Author: Sindhu Govindareddy Doddamane

SIM_DIR  = ../sim
RTL_DIR  = ../rtl
TB_DIR   = ../tb

# Default target
all: compile simulate coverage

# Compile
compile:
	@echo "Compiling RTL and Testbench..."
	iverilog -g2012 -o $(SIM_DIR)/fifo_sim \
		$(RTL_DIR)/fifo.sv \
		$(TB_DIR)/fifo_tb.sv
	@echo "Compilation DONE ✅"

# Simulate
simulate:
	@echo "Running Simulation..."
	vvp $(SIM_DIR)/fifo_sim | tee $(SIM_DIR)/sim_results.log
	@echo "Simulation DONE ✅"

# Coverage Report
coverage:
	@echo "Generating Coverage Report..."
	python3 ../coverage/parse_coverage.py \
		$(SIM_DIR)/sim_results.log
	@echo "Coverage Report DONE ✅"

# Clean
clean:
	@echo "Cleaning up..."
	rm -f $(SIM_DIR)/fifo_sim
	rm -f $(SIM_DIR)/*.vcd
	rm -f $(SIM_DIR)/*.log
	@echo "Clean DONE ✅"
