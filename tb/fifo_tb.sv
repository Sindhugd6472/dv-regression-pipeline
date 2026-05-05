// FIFO Testbench
// Author: Sindhu Govindareddy Doddamane

`timescale 1ns/1ps

module fifo_tb;

  // Parameters
  parameter DEPTH = 8;
  parameter WIDTH = 8;

  // Signals
  logic             clk;
  logic             rst_n;
  logic             wr_en;
  logic             rd_en;
  logic [WIDTH-1:0] din;
  logic [WIDTH-1:0] dout;
  logic             full;
  logic             empty;

  // Instantiate DUT
  fifo #(.DEPTH(DEPTH), .WIDTH(WIDTH)) dut (
    .clk   (clk),
    .rst_n (rst_n),
    .wr_en (wr_en),
    .rd_en (rd_en),
    .din   (din),
    .dout  (dout),
    .full  (full),
    .empty (empty)
  );

  // Clock Generation: 10ns period
  initial clk = 0;
  always #5 clk = ~clk;

  // Coverage Groups
  covergroup fifo_cg @(posedge clk);
    cp_full  : coverpoint full  { bins full_high  = {1}; bins full_low  = {0}; }
    cp_empty : coverpoint empty { bins empty_high = {1}; bins empty_low = {0}; }
    cp_wr_en : coverpoint wr_en { bins wr_high    = {1}; bins wr_low    = {0}; }
    cp_rd_en : coverpoint rd_en { bins rd_high    = {1}; bins rd_low    = {0}; }
  endgroup

  fifo_cg cg_inst = new();

  // Tasks
  task write_fifo(input logic [WIDTH-1:0] data);
    @(posedge clk);
    wr_en = 1;
    din   = data;
    @(posedge clk);
    wr_en = 0;
  endtask

  task read_fifo();
    @(posedge clk);
    rd_en = 1;
    @(posedge clk);
    rd_en = 0;
  endtask

  // Main Test
  integer pass_count = 0;
  integer fail_count = 0;

  initial begin
    // Init
    rst_n = 0; wr_en = 0; rd_en = 0; din = 0;
    repeat(2) @(posedge clk);
    rst_n = 1;

    // Test 1: Write until FULL
    $display("\n--- Test 1: Fill FIFO ---");
    repeat(DEPTH) begin
      write_fifo($random);
    end
    if (full) begin
      $display("PASS: FIFO is FULL as expected"); pass_count++;
    end else begin
      $display("FAIL: FIFO should be FULL"); fail_count++;
    end

    // Test 2: Write when FULL (should be ignored)
    $display("\n--- Test 2: Write when FULL ---");
    write_fifo(8'hFF);
    if (full) begin
      $display("PASS: Write ignored when FULL"); pass_count++;
    end else begin
      $display("FAIL: Overflow occurred"); fail_count++;
    end

    // Test 3: Read until EMPTY
    $display("\n--- Test 3: Drain FIFO ---");
    repeat(DEPTH) begin
      read_fifo();
    end
    if (empty) begin
      $display("PASS: FIFO is EMPTY as expected"); pass_count++;
    end else begin
      $display("FAIL: FIFO should be EMPTY"); fail_count++;
    end

    // Test 4: Read when EMPTY (should be ignored)
    $display("\n--- Test 4: Read when EMPTY ---");
    read_fifo();
    if (empty) begin
      $display("PASS: Read ignored when EMPTY"); pass_count++;
    end else begin
      $display("FAIL: Underflow occurred"); fail_count++;
    end

    // Test 5: Simultaneous Read/Write
    $display("\n--- Test 5: Simultaneous Read/Write ---");
    write_fifo(8'hAA);
    @(posedge clk);
    wr_en = 1; rd_en = 1; din = 8'hBB;
    @(posedge clk);
    wr_en = 0; rd_en = 0;
    $display("PASS: Simultaneous RD/WR completed"); pass_count++;

    // Summary
    $display("\n================================");
    $display("  TEST SUMMARY");
    $display("  PASSED : %0d", pass_count);
    $display("  FAILED : %0d", fail_count);
    $display("================================\n");

    // Coverage Report
    $display("Functional Coverage: %0.2f%%", cg_inst.get_coverage());

    $finish;
  end

  // Waveform dump
  initial begin
    $dumpfile("sim/fifo_tb.vcd");
    $dumpvars(0, fifo_tb);
  end

endmodule
