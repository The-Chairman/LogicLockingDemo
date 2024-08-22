// Verilog
// kmStLN
// Ninputs 5
// Noutputs 4
// NtotalGates 45
// BUF1 4
// NOT1 9
// NAND2 32

module  kmStLN (N1,N4,N8,N11,N14,N90,N91,N92,N93);

input N1,N4,N8,N11,N14;

output N90,N91,N92,N93;

wire N115,N116,N117,N118,N119,N123,N124,N125,N126,N216,
     N217,N218,N219,N223,N224,N225,N226,N316,N317,N318,
     N319,N323,N324,N325,N326,N416,N417,N418,N419,N423,
     N424,N425,N426;

not  NOT1_1 (N115, N14);
not  NOT1_2 (N116, N11);
not  NOT1_3 (N117, N118);
nand NAND2_4 (N124, N11, N115);
nand NAND2_5 (N123, N116, N115);
nand NAND2_6 (N119, N118, N123);
nand NAND2_7 (N118, N119, N124);
nand NAND2_8 (N124, N118, N14);
nand NAND2_9 (N123, N117, N14);
nand NAND2_10 (N125, N126, N123);
nand NAND2_11 (N126, N125, N124);
not  NOT1_12 (N216, N8);
not  NOT1_13 (N217, N218);
nand NAND2_14 (N224, N8, N115);
nand NAND2_15 (N223, N216, N115);
nand NAND2_16 (N219, N218, N223);
nand NAND2_17 (N218, N219, N224);
nand NAND2_18 (N224, N218, N14);
nand NAND2_19 (N223, N217, N14);
nand NAND2_20 (N225, N226, N223);
nand NAND2_21 (N226, N225, N224);
not  NOT1_22 (N316, N4);
not  NOT1_23 (N317, N318);
nand NAND2_24 (N324, N4, N115);
nand NAND2_25 (N323, N316, N115);
nand NAND2_26 (N319, N318, N323);
nand NAND2_27 (N318, N319, N324);
nand NAND2_28 (N324, N318, N14);
nand NAND2_29 (N323, N317, N14);
nand NAND2_30 (N325, N326, N323);
nand NAND2_31 (N326, N325, N324);
not  NOT1_32 (N416, N1);
not  NOT1_33 (N417, N418);
nand NAND2_34 (N424, N1, N115);
nand NAND2_35 (N423, N416, N115);
nand NAND2_36 (N419, N418, N423);
nand NAND2_37 (N418, N419, N424);
nand NAND2_38 (N424, N418, N14);
nand NAND2_39 (N423, N417, N14);
nand NAND2_40 (N425, N426, N423);
nand NAND2_41 (N426, N425, N424);
buf BUF_42 (N90, N126);
buf BUF_43 (N91, N226);
buf BUF_44 (N92, N326);
buf BUF_45 (N93, N426);

endmodule


