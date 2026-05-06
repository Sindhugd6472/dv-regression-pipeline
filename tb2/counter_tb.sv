// Counter Testbench
// Author: Sindhu Govindareddy Doddamane

`timescale 1ns/1ps

module counter_tb;

  parameter WIDTH = 4;

  logic             clk;
  logic             rst_n;
  logic             enable;
  logic             up_down;
  logic             load;
  logic [WIDTH-1:0] load_val;
  logic [WIDTH-1:0] count;
  logic             overflow;
  logic             underflow;

  // Instantiate DUT
  counter #(.WIDTH(WIDTH)) dut (
    .clk      (clk),
    .rst_n    (rst_n),
    .enable   (enable),
    .up_down  (up_down),
    .load     (load),
    .load_val (load_val),
    .count    (count),
    .overflow (overflow),
    .underflow(underflow)
  );

  // Clock
  initial clk = 0;
  always #5 clk = ~clk;

  // Coverage tracking
  integer cov_up_seen       = 0;
  integer cov_down_seen     = 0;
  integer cov_overflow_seen = 0;
  integer cov_load_seen     = 0;

  always @(posedge clk) begin
    if (up_down && enable) cov_up_seen       = 1;
    if (!up_down && enable) cov_down_seen    = 1;
    if (overflow)           cov_overflow_seen = 1;
    if (load)               cov_load_seen     = 1;
  end

  integer pass_count = 0;
  integer fail_count = 0;

  initial begin
    // Init
    rst_n = 0; enable = 0; up_down = 1;
    load = 0; load_val = 0;
    repeat(2) @(posedge clk);
    rst_n = 1;

    // Test 1: Count Up
    $display("\n--- Test 1: Count Up ---");
    enable = 1; up_down = 1;
    repeat(5) @(posedge clk);
    enable = 0;
    if (count == 5) begin
      $display("PASS: Count up to 5 correctly"); pass_count++;
    end else begin
      $display("FAIL: Count up failed, got %0d", count); fail_count++;
    end

    // Test 2: Count Down
    $display("\n--- Test 2: Count Down ---");
    enable = 1; up_down = 0;
    repeat(3) @(posedge clk);
    enable = 0;
    if (count == 2) begin
      $display("PASS: Count down to 2 correctly"); pass_count++;
    end else begin
      $display("FAIL: Count down failed, got %0d", count); fail_count++;
    end

    // Test 3: Load Value
    $display("\n--- Test 3: Load Value ---");
    load = 1; load_val = 4'hA;
    @(posedge clk);
    load = 0;
    if (count == 4'hA) begin
      $display("PASS: Load value 10 correctly"); pass_count++;
    end else begin
      $display("FAIL: Load failed, got %0d", count); fail_count++;
    end

    // Test 4: Overflow Detection
    $display("\n--- Test 4: Overflow Detection ---");
    load = 1; load_val = 4'hE;
    @(posedge clk);
    load = 0;
    enable = 1; up_down = 1;
    @(posedge clk);
    if (overflow) begin
      $display("PASS: Overflow detected correctly"); pass_count++;
    end else begin
      $display("FAIL: Overflow not detected"); fail_count++;
    end
    enable = 0;

    // Test 5: Reset
    $display("\n--- Test 5: Reset ---");
    rst_n = 0;
    @(posedge clk);
    rst_n = 1;
    if (count == 0) begin
      $display("PASS: Reset works correctly"); pass_count++;
    end else begin
      $display("FAIL: Reset failed, got %0d", count); fail_count++;
    end

    // Summary
    $display("\n================================");
    $display("  TEST SUMMARY");
    $display("  PASSED : %0d", pass_count);
    $display("  FAILED : %0d", fail_count);
    $display("================================\n");

    // Coverage
    begin
      integer cov_total;
      cov_total = cov_up_seen + cov_down_seen +
                  cov_overflow_seen + cov_load_seen;
      $display("Functional Coverage: %0.2f%%",
               (cov_total / 4.0) * 100.0);
    end

    $finish;
  end

  initial begin
    $dumpfile("sim/counter_tb.vcd");
    $dumpvars(0, counter_tb);
  end

endmodule
