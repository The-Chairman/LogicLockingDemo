modules = kSLN kmStLN koStLN wmStLN woStLN c432
sub_command=all

all: $(modules) llocking.html

llocking.html:	$(foreach h,$(modules), $(h)/$(h).html)
	python bin/gen_main.py -f $@

output.xlsx:
	for e in $(modules) ; do\
		python ./bin/crunch_stats.py -d $$e -o $@ ; \
	done
	
%/%.html:
	for e in $(modules) ; do\
		$(MAKE) -C $$e -f ../circuit.mak module=$$e $$e.html ; \
	done	

.PHONY: $(modules) STATUS_ALL CLEAN_ALL CLEAN_REPORTS CLEAN_IMAGES

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
	
CLEAN_REPORTS:
	for e in $(modules) ; do\
		rm -f $$e/$$e.html ; \
	done
	rm llocking.html

CLEAN_IMAGES:
	for e in $(modules) ; do\
		$(MAKE) -C $$e -f ../circuit.mak module=$$e clean_netlist_svg ; \
	done