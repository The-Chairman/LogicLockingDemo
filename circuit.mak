BIN_DIR=../bin

yosys_generated_files= .dot .svg _stats.json _netlist.json
#unlocked_files= unlocked/$(module)_unlocked.v unlocked/$(module)_unlocked.dot unlocked/$(module)_unlocked.svg unlocked/$(module)_unlocked_stats.json unlocked/$(module)_unlocked_netlist.json unlocked/$(module)_unlocked_netlist.svg
unlocked_files= $(foreach e,$(yosys_generated_files),unlocked/$(module)_unlocked$(e)) unlocked/$(module)_unlocked_netlist.svg
enabled=$(shell python -c 'import json; fin = open( "lock_config.json", "r") ; config=json.load(fin) ; print( " ".join( config["enabled"].keys())); fin.close()')
disabled=$(shell python -c 'import json; fin = open( "lock_config.json", "r") ; config=json.load(fin) ; print( " ".join( config["disabled"].keys())); fin.close()')

enabled_verilog=$(foreach ll,$(enabled),$(ll)/$(file_main)_$(ll).v)

all_locks=$(enabled) $(disabled)

define LOCKED_VERILOG_MACRO
$(1): $(1)/$(module)_$(1).v $(foreach e,$(yosys_generated_files),$(1)/$(module)_$(1)$(e)) $(1)/$(module)_$(1)_netlist.svg

$(1)/$(module)_$(1).v: unlocked/$(module)_unlocked.v
	mkdir -p $(1)
	python ../logiclock_wrapper.py -f $$< -d $(1) -l $(1) -b $(module)

$(foreach e,$(yosys_generated_files),$(1)/$(module)_$(1)$(e)) : $(1)/$(module)_$(1).v
	bash $(BIN_DIR)/yosys_build.sh $(1)/$(module)_$(1).v $(module) $(1) $(module)_$(1)
endef

all: unlocked $(enabled)

.PHONY: unlocked all_locks test clean clean_netlist_svg status

unlocked: $(unlocked_files)
all_locks: $(all_locks) $(experimental_targets)
	
unlocked/$(module)_unlocked.v: $(module).v
	mkdir -p unlocked
	cp $< $@

$(foreach i,$(enabled),$(eval $(call LOCKED_VERILOG_MACRO,$i)))

#unlocked/$(module)_unlocked.dot unlocked/$(module)_unlocked.svg unlocked/$(module)_unlocked_stats.json unlocked/$(module)_unlocked_netlist.json: unlocked/$(module)_unlocked.v
$(foreach e,$(yosys_generated_files),unlocked/$(module)_unlocked$(e)): unlocked/$(module)_unlocked.v
	bash $(BIN_DIR)/yosys_build.sh unlocked/$(module)_unlocked.v $(RUN_YOSYS) $(module) unlocked $(module)_unlocked

%_netlist.svg: %_netlist.json
	netlistsvg $< -o $@ --skin ../resources/circuit_diagram_skin.svg

# Stats #######################################################################
status:
	@printf '%80s\n' | tr ' ' '#'
	@echo "\033[0;31mDisabled Locks\033[0m"
	@for i in $(disabled); do echo "$$i"; done
	@echo

	@echo "\033[0;32mEnabled Locks\033[0m" ;
	@for i in unlocked $(enabled); do \
		for j in $(foreach e,$(yosys_generated_files) .v .svg _netlist.svg, $$i/$(module)_$${i}${e}); do \
			echo -n $$j... ;  \
			if [ -f $$j ]; then echo "\033[0;32mexists\033[0m" ; \
			else echo "\033[0;31mmissing\033[0m" ; fi \
		done ; \
	done
	@echo

# Clean #######################################################################
clean:
	@for i in unlocked $(enabled) ; do \
		if [ -d $$i ] ; then rm -rf $$i/ ; else echo "$$i is missing" ; fi \
	done

 clean_netlist_svg:
	@for i in `find . -type f -name "*_netlist.svg"` ; do \
		rm $$i ; \
	done