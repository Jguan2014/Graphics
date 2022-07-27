//Pseudocode for anti-alising FPGA implementation 

module aa(parameter bitwidth = 10)(
  logic                 clk,
  logic                 reset_n,
  logic [size-1: 0]     frame [size-1:0],
  logic [bitwidth-1:0]  th,
  logic                 done
);
 
  logic [size-1: 0] avg_frame [size-1:0],
  genvar row, col;
  
  always @(posedge clk or negedge reset_n) begin 
    if (!reset_n) begin
        row = 1;
        col = 1;
    end else begin 
      generate 
        for (row = 0; row < size-1; row = row+1) begin 
          for (col = 0; col < size-1; col = col+1) begin 
              if (frame[row][col] > th && (frame[row+1][col] < th || frame[row-1][col] < th || frame[row][col+1] < th || frame[row][col-1] < th)) begin 
                avg_frame[row][col] <= (frame[row][col] + frame[row+1][col] + frame[row-1][col] + frame[row][col+1] + frame[row][col-1]) >> 4 //if it is a black pixel neighbours a white pixel
                //calculate the avg of the neighbouring pixels and divide by 4, shift right twice is easier/efficient that divide by 5
              end 
            end 
          end 
      endgenerate 
    end 
  end 
    
      assign done = (row == size-1 && col == size-1)? 1 : 0; //assert done when the whole frame has been processed 
   
    endmodule 
