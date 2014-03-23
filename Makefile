DEMOS=\
 0    \
 1    \
 2    \
 3    \
 4    \
 5    \
 6    \
 7    

all:
	@for demo in $(DEMOS); do \
	  $(MAKE) -C $$demo;      \
	done

clean:
	@for demo in $(DEMOS); do  \
	  $(MAKE) -C $$demo clean; \
	done
