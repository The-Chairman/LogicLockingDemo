// Verilog
// kSLN
// Ninputs 8
// Noutputs 4
// NtotalGates 8
// BUF1 4
// AND4 1
// OR3 1
// XOR2 1
// AND3 1

module  kSLN (N1,N4,N8,N11,N14,N17,N21,N24,N27,N223,N329,N370,N421);

input N1,N4,N8,N11,N14,N17,N21,N24,N27;

output N223,N329,N370,N421;

wire N118,N119,N122,N123;

and AND4_1 (N118, N17, N21, N24, N27);
or  OR3_2  (N119, N11, N14, N17);
xor XOR2_3 (N122, N8, N11);
and AND3_4 (N123, N1, N4, N8);

buf BUF_5 (N223, N118);
buf BUF_6 (N329, N119);
buf BUF_7 (N370, N122);
buf BUF_8 (N421, N123);

endmodule


