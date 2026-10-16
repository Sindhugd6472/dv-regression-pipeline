`timescale 1ns/1ps
module fifo_tb;
  parameter DEPTH = 8;
  parameter WIDTH = 8;
  logic clk = 0;
  always #5 clk = ~clk;
  logic rst_n = 0, wr_en = 0, rd_en = 0;
  logic [WIDTH-1:0] din = 0, dout;
  logic full, empty;
  fifo #(.DEPTH(DEPTH), .WIDTH(WIDTH)) dut(.*);
  logic [WIDTH-1:0] model [0:DEPTH-1];
  logic [WIDTH-1:0] expected_dout = 0;
  integer head = 0, tail = 0, used = 0;
  integer pass_count = 0;
  integer cov_full_seen = 0, cov_empty_seen = 0, cov_wr_seen = 0, cov_rd_seen = 0;

  // Drive away from the active edge and compare after nonblocking updates.
  task automatic cycle(input bit wr, input bit rd, input logic [WIDTH-1:0] data);
    bit take_write, take_read;
    @(negedge clk);
    wr_en = wr; rd_en = rd; din = data;
    take_write = wr && used < DEPTH;
    take_read = rd && used > 0;
    if (take_read) begin
      expected_dout = model[head];
      head = (head + 1) % DEPTH;
    end
    if (take_write) begin
      model[tail] = data;
      tail = (tail + 1) % DEPTH;
    end
    used = used + int'(take_write) - int'(take_read);
    @(posedge clk); #1;
    if (dout !== expected_dout || full !== (used == DEPTH) || empty !== (used == 0))
      $fatal(1, "FAIL: FIFO mismatch used=%0d dout=%h expected=%h full=%b empty=%b", used, dout, expected_dout, full, empty);
    cov_full_seen |= full;
    cov_empty_seen |= empty;
    cov_wr_seen |= take_write;
    cov_rd_seen |= take_read;
    pass_count++;
  endtask

  initial begin
    repeat (2) @(negedge clk);
    rst_n = 1;
    #1;
    if (empty !== 1 || full !== 0 || dout !== 0) $fatal(1, "FAIL: Reset");
    // Multiple fill/drain rounds expose pointer wrap and ordering errors.
    repeat (4) begin
      repeat (DEPTH) cycle(1, 0, $random);
      cycle(1, 0, '1); // overflow ignored
      repeat (DEPTH) cycle(0, 1, 0);
      cycle(0, 1, 0); // underflow ignored
    end
    cycle(1, 1, 'hAA); // empty boundary accepts only write
    repeat (DEPTH*4) cycle(1, 1, $random);
    repeat (DEPTH*40) cycle($random, $random, $random);
    while (used > 0) cycle(0, 1, 0);
    // Reset while nonempty also clears pointers, count, and output.
    cycle(1, 0, 'h55);
    @(negedge clk); rst_n = 0; wr_en = 0; rd_en = 0;
    #1;
    if (empty !== 1 || full !== 0 || dout !== 0) $fatal(1, "FAIL: Midstream reset");
    head = 0; tail = 0; used = 0; expected_dout = 0;
    @(negedge clk); rst_n = 1;
    cycle(1, 0, 'h5A); cycle(0, 1, 0);
    $display("PASS: FIFO ordering, wrap, boundaries, simultaneous operations and reset (%0d checks)", pass_count);
    $display("Functional Coverage: %0.2f%%", (cov_full_seen + cov_empty_seen + cov_wr_seen + cov_rd_seen) * 25.0);
    $finish;
  end
  initial begin
    #1000000; $fatal(1, "FAIL: FIFO timeout");
  end
endmodule
