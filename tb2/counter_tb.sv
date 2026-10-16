`timescale 1ns/1ps
module counter_tb;
  parameter WIDTH=4;
  logic clk=0; always #5 clk=~clk;
  logic rst_n=0,enable=0,up_down=1,load=0;
  logic [WIDTH-1:0] load_val=0,count,expected=0;
  logic overflow,underflow;
  counter #(.WIDTH(WIDTH)) dut(.*);
  integer checks=0;
  bit cov_load=0,cov_hold=0,cov_up=0,cov_down=0,cov_overflow=0,cov_underflow=0;
  task automatic cycle(input bit en,input bit up,input bit ld,input logic [WIDTH-1:0] value);
    @(negedge clk);enable=en;up_down=up;load=ld;load_val=value;
    #1;
    if (overflow !== ((&expected) && en && up) ||
        underflow !== ((expected == 0) && en && !up))
      $fatal(1,"FAIL: Counter boundary flags");
    cov_load |= ld;
    cov_hold |= !en && !ld;
    cov_up |= en && up && !ld;
    cov_down |= en && !up && !ld;
    cov_overflow |= overflow;
    cov_underflow |= underflow;
    if(ld) expected=value;
    else if(en) expected=up ? expected+1'b1 : expected-1'b1;
    @(posedge clk);#1;
    if(count !== expected) $fatal(1,"FAIL: Counter got=%h expected=%h",count,expected);
    checks++;
  endtask
  initial begin
    repeat(2) @(negedge clk);rst_n=1;
    cycle(0,1,0,0); // hold
    cycle(1,1,1,'1); // load priority
    cycle(1,1,0,0); // overflow and wrap
    cycle(1,0,0,0); // underflow and wrap
    cycle(1,0,1,0);
    repeat(100) cycle($random,$random,$random,$random);
    @(negedge clk);rst_n=0;
    #1;if(count !== 0) $fatal(1,"FAIL: Counter reset");
    $display("PASS: Counter load priority, hold, directions, wrap, flags, reset (%0d checks)",checks);
    $display("Functional Coverage: %0.2f%%", (int'(cov_load)+int'(cov_hold)+int'(cov_up)+int'(cov_down)+int'(cov_overflow)+int'(cov_underflow))*100.0/6.0);
    $finish;
  end
  initial begin #100000;$fatal(1,"FAIL: Counter timeout");end
endmodule
