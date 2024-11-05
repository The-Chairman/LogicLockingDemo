
verilog_file=$1
top_module=$2
output_dir=$3
schematic_basename=$4

f=`mktemp /tmp/schematic.XXXXXX`
echo "temp file $f"
cat << EOF > $f
read_verilog -sv -formal ${verilog_file};
hierarchy -check -top ${top_module};
hierarchy -generate;
proc; opt; memory; opt; fsm; opt; techmap; opt;
synth;
opt_clean;
clean -purge;
tee -o ${output_dir}/${schematic_basename}_stats.json stat -json;
show -prefix  ${output_dir}/${schematic_basename} -notitle -colors 2 -width -format dot -stretch -enum  -color darkgreen i:key_* -color darkred o:*;
show -prefix  ${output_dir}/${schematic_basename} -notitle -colors 2 -width -format svg -stretch -enum  -color darkgreen i:key_* -color darkred o:*;
write_json ${output_dir}/${schematic_basename}_netlist.json
EOF

yosys -s ${f}
rm $f