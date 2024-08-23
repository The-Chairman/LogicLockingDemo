modules = kSLN kmStLN koStln wmStLN woStLN 

all: 
	@for i in $(modules); do\
			cd $$i && $(MAKE) && cd ..;\
	done;


.PHONY: copy status

copy:
	@for i in $(modules); do\
			cd $$i && $(MAKE) copy && cd ..;\
	done;

status:
	@for i in $(modules); do\
			cd $$i && $(MAKE) status && cd ..;\
	done;

