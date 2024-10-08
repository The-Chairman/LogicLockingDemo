// Verilog
// koStLN
// Ninputs 5
// Noutputs 4
// NtotalGates 28
// BUF1 4
// NAND2 20
// NAND3 4

module  koStLN (N1,N4,N8,N11,N14,N555,N329,N370,N421);

input N1,N4,N8,N11,N14;

output N555,N329,N370,N421;

wire N118,N119,N123,N124,N125,N126,N218,N219,
     N223, N224,N225,N226,N248,N249,N243,N244,N245,
     N246,N250,N251,N253,N254,N255,N256;

nand NAND2_1 (N126, N125, N124);
nand NAND2_2 (N125, N11, N123);
nand NAND2_3 (N124, N126, N14);
nand NAND3_4 (N123, N124, N125, N14);
nand NAND2_5 (N119, N118, N123);
nand NAND2_6 (N118, N119, N124);
nand NAND2_7 (N226, N225, N224);
nand NAND2_8 (N225, N8, N223);
nand NAND2_9 (N224, N226, N14);
nand NAND3_10 (N223, N224, N225, N14);
nand NAND2_11 (N219, N218, N223);
nand NAND2_12 (N218, N219, N224);
nand NAND2_13 (N246, N245, N244);
nand NAND2_14 (N245, N4, N243);
nand NAND2_15 (N244, N246, N14);
nand NAND3_16 (N243, N244, N245, N14);
nand NAND2_17 (N249, N248, N243);
nand NAND2_18 (N248, N249, N244);
nand NAND2_19 (N256, N255, N254);
nand NAND2_20 (N255, N1, N253);
nand NAND2_21 (N254, N256, N14);
nand NAND3_22 (N253, N254, N255, N14);
nand NAND2_23 (N251, N250, N253);
nand NAND2_24 (N250, N251, N254);
buf BUF_25 (N555, N118);
buf BUF_26 (N329, N218);
buf BUF_27 (N370, N248);
buf BUF_28 (N421, N250);

endmodule


