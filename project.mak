modules = kSLN kmStLN koStLN wmStLN woStLN c432
sub_command=all

all: $(modules)

science_day_2024/llocking.html: $(foreach module,$(modules),science_day_2024/$(module)/$(module).html)
	python bin/gen_main.py -f $@ -t science_day_2024/html_templates

 $(foreach module,$(modules),science_day_2024/$(module)/$(module).html):
	@mkdir -p $(dir $@)
	cd $(basename $(notdir $@)) && python ../bin/gen_index.py -b $(basename $(notdir $@)) -f ../$@ -t ../science_day_2024/html_templates	
output.xlsx:
	for e in $(modules) ; do\
		python ./bin/crunch_stats.py -d $$e -o $@ ; \
	done
	
%/%.html:
	for e in $(modules) ; do\
		$(MAKE) -C $$e -f ../circuit.mak module=$$e $$e.html ; \
	done	

.PHONY: $(modules) STATUS_ALL CLEAN_ALL CLEAN_REPORTS CLEAN_IMAGES SCIENCE_DAY_24

$(modules):
	$(MAKE) -C $@ -f ../circuit.mak module=$@ $(sub_command)

STATUS_ALL:
	for e in $(modules) ; do\
		$(MAKE) -C $$e -f ../circuit.mak module=$$e status ; \
	done

CLEAN_ALL:
	for e in $(modules) ; do\
		$(MAKE) -C $$e -f ../circuit.mak module=$$e clean ; \
	done
	
CLEAN_SCIENCE_DAY_24:
	for e in `find science_day_2024/ -name *.html ! -path '*html_templates/*.html' ! -path *locking_info.html` ; do\
		rm $$e ; \
	done

CLEAN_IMAGES:
	for e in $(modules) ; do\
		$(MAKE) -C $$e -f ../circuit.mak module=$$e clean_netlist_svg ; \
	done

SCIENCE_DAY_24: science_day_2024/llocking.html $(foreach module,$(modules),science_day_2024/$(module)/$(module).html)