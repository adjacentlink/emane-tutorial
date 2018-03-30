DEMOS=\
 0    \
 1    \
 2    \
 3    \
 5    \
 6    \
 7    \
 8

all:
	@for demo in $(DEMOS); do \
	  $(MAKE) -C $$demo;      \
	done

clean:
	@for demo in $(DEMOS); do  \
	  $(MAKE) -C $$demo clean; \
	done
