file_main = c432
module_top = c432
odir = ../test_output/$(module_top)
all_locks = full_lock full_lock_mux lut_lock mux_lock random_lut_lock sfll_flex sfll_hd tt_lock tt_lock_sen xor_lock
broken_locks = trll
locked_verilog=$(foreach ll,$(all_locks),$(ll)/$(file_main)_$(ll)_locked.v)
locked_keys=$(foreach ll,$(all_locks),$(ll)/$(file_main)_$(ll)_locked_key.txt)
locked_dot=$(foreach ll,$(all_locks),$(ll)/$(file_main)_$(ll)_locked.dot)
locked_svg=$(foreach ll,$(all_locks),$(ll)/$(file_main)_$(ll)_locked.svg)

all: $(file_main).dot\
		$(file_main).svg\
		$(locked_verilog)\
		$(locked_dot)\
		$(locked_svg)\
		$(file_main).html

$(file_main).html:
	python ../gen_index.py -b $(file_main) -f $@ -t ../html_templates

%.v:
	mkdir -p $(dir $@)
	python ../logiclock_wrapper.py -f $(file_main).v -d $(dir $@) -l $(subst _locked,, $(subst $(file_main)_,,$(basename $(notdir $@))))


%.dot: %.v
	cd $(dir $@) ; yosys \
		-p "read_verilog -sv -formal $(notdir $<)" \
		-p "hierarchy -check -top $(module_top)" \
		-p "hierarchy -generate" \
		-p "show -prefix  $(basename $(notdir $@)) -notitle -colors 2 -width -format dot -stretch -enum"

%.svg: %.dot
	dot -Tsvg -o $@ $*.dot

.PHONY: copy locked_verilog clean clean_schematics $(all_locks) locked_dot locked_svg status

$(all_locks): % : $(file_main)_%_locked.svg

copy:
	mkdir -p $(odir)
	@for i in $(file_main).v \
	$(file_main).dot \
	$(file_main).svg \
	$(locked_verilog) \
	$(locked_keys) \
	$(locked_svg) \
	$(file_main).html;do\
		if [ -f $$i ]; then cp $$i $(odir); fi \
	done
locked_verilog: $(locked_verilog)

locked_dot: $(locked_dot)

locked_svg: $(locked_svg)

clean:
	@for i in $(file_main).dot $(file_main).svg $(locked_verilog) $(locked_dot) \
	$(locked_svg) $(locked_keys);do\
			rm -f $$i; \
	done

clean_schematics:
	@for i in $(file_main).dot $(file_main).svg $(locked_dot) $(locked_svg); do\
			rm -f $$i; \
	done

status:
	@for i in $(file_main).v \
	$(file_main).dot \
	$(file_main).svg \
	$(locked_verilog) \
	$(locked_keys) \
	$(locked_svg);do\
		echo -n "$$i..." ; \
		if [ -f $$i ]; then echo "\033[0;32mexists\033[0m" ; \
		else echo "\033[0;31mmissing\033[0m" ; fi \
	done
	@echo ""
	@for i in $(broken_locks); do\
			echo "$$i...broken"; \
	done
