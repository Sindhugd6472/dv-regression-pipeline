// Synchronous Up/Down Counter
// 4-bit, with load, enable, and overflow detection
// Author: Sindhu Govindareddy Doddamane

module counter #(
  parameter WIDTH = 4
)(
  input  logic             clk,
  input  logic             rst_n,
  input  logic             enable,
  input  logic             up_down,  // 1=up, 0=down
  input  logic             load,
  input  logic [WIDTH-1:0] load_val,
  output logic [WIDTH-1:0] count,
  output logic             overflow,
  output logic             underflow
);

  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      count <= 0;
    end else if (load) begin
      count <= load_val;
    end else if (enable) begin
      if (up_down)
        count <= count + 1;
      else
        count <= count - 1;
    end
  end

  assign overflow  = (count == 4'hF) && enable && up_down;
  assign underflow = (count == 4'h0) && enable && !up_down;

endmodule
