modules = kSLN kmStLN koStLN wmStLN woStLN c432
sub_command=all

all: $(modules) llocking.html

llocking.html:	$(foreach h,$(modules), $(h)/$(h).html)
	python bin/gen_main.py -f $@

%/%.html:
	for e in $(modules) ; do\
		$(MAKE) -C $$e -f ../circuit.mak module=$$e $$e.html ; \
	done	

.PHONY: $(modules) STATUS_ALL CLEAN_ALL

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