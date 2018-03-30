# verify TOP_DIR is defined
ifeq ($(origin TOP_DIR), undefined)
$(error TOP_DIR must be defined)
endif

# Template for emane application XML files
TEMPLATE_PLATFORM ?= $(TOP_DIR)/templates/platform.xml.template

# Template for emaneeventd application XML files
TEMPLATE_EVENTDAEMON ?= $(TOP_DIR)/templates/eventdaemon.xml.template

# Template for gpsdlocationagent XML
TEMPLATE_GPSDLOCATIONAGENT ?= $(TOP_DIR)/templates/gpsdlocationagent.xml.template

# Template for mgen input files
TEMPLATE_MGEN ?= $(TOP_DIR)/templates/mgen.template

# Template for routing input conf files
TEMPLATE_ROUTING ?= $(TOP_DIR)/templates/routing.conf.template

# Template for starting demo on remote nodes
TEMPLATE_DEMOSTART ?= $(TOP_DIR)/templates/demo-start.template

# Template for stopping demo on remote nodes
TEMPLATE_DEMOSTOP ?= $(TOP_DIR)/templates/demo-stop.template

PLATFORMDEPS=$(GENERATED_PLATFORMS:%=.%-dep) $(PLATFORMS:%=.%-dep)

# Template for srw radio XML files
TEMPLATE_OTESTPOINTD ?= $(TOP_DIR)/templates/otestpointd.xml.template

# Template for srw radio XML files
TEMPLATE_OTESTPOINTRECORDER ?= $(TOP_DIR)/templates/otestpoint-recorder.xml.template

.PHONY:	all clean verify

all:  $(GENERATED_EXTRA) $(PLATFORMDEPS) $(GENERATED_EVENTDAEMONS) \
      $(GENERATED_GPSDLOCATIONAGENTS) $(GENERATED_MGENINPUTS) \
      $(GENERATED_ROUTINGCONFS) $(GENERATED_OTESTPOINTDS) \
      $(GENERATED_OTESTPOINTRECORDERS) demo-start demo-stop 
	$(MAKE) all-local

all-local:

verify:
	xmllint --noout --valid *.xml

edit= sed -e 's|@NEMID[@]|$*|g' \
          -e 's|@NODEID[@]|$*|g' \
          -e 's|@NODEIDHEX[@]|$(shell printf "%02x" $*)|g' \
          -e 's|@DEMOID[@]|$(DEMO_ID)|g' \
          -e 's|@NEMXML[@]|$(NEM_XML)|g ' \
          -e 's|@TOPDIR[@]|$(shell dirname $$(pwd))|g' \
          -e 's|@OLSRTXTINFO[@]|$(shell basename \
                 $$(find /usr/lib* -name "olsrd_txtinfo.so*" -print 2> /dev/null))|g' \
          -e 's|@NODECOUNT[@]|$(shell if [ -n "$(NODE_COUNT)" ]; \
                                      then \
                                        echo $(NODE_COUNT); \
                                      else \
                                        echo $(PLATFORMDEPS)| wc -w; \
                                      fi)|g'

ifdef GENERATED_PLATFORMS

platform%.xml: $(TEMPLATE_PLATFORM)
	if test -f $@; then chmod u+w $@; fi
	$(edit) $< > $@
	chmod g-w,u-w $@

endif

$(PLATFORMDEPS): .%-dep:%
	mkdir .emanegentransportxml && \
	 cd .emanegentransportxml &&   \
	 emanegentransportxml ../$< && \
	 for i in $$(ls *.xml); do chmod g-w,u-w $$i; cp -f $$i ..; done && \
	 cd .. && \
	 rm -rf .emanegentransportxml
	@touch $@

eventdaemon%.xml: $(TEMPLATE_EVENTDAEMON)
	if test -f $@; then chmod u+w $@; fi
	$(edit) $< > $@
	chmod g-w,u-w $@

gpsdlocationagent%.xml: $(TEMPLATE_GPSDLOCATIONAGENT)
	if test -f $@; then chmod u+w $@; fi
	$(edit) $< > $@
	chmod g-w,u-w $@

mgen%: $(TEMPLATE_MGEN)
	if test -f $@; then chmod u+w $@; fi
	$(edit) $< > $@
	chmod g-w,u-w $@

routing%.conf: $(TEMPLATE_ROUTING)
	if test -f $@; then chmod u+w $@; fi
	$(edit) $< > $@
	chmod g-w,u-w $@

otestpointd%.xml: $(TEMPLATE_OTESTPOINTD)
	if test -f $@; then chmod u+w $@; fi
	$(edit) $< > $@
	chmod g-w,u-w $@

otestpoint-recorder%.xml: $(TEMPLATE_OTESTPOINTRECORDER)
	if test -f $@; then chmod u+w $@; fi
	$(edit) $< > $@
	chmod g-w,u-w $@

demo-start: $(TEMPLATE_DEMOSTART)
	if test -f $@; then chmod u+w $@; fi
	$(edit) $< > $@
	chmod g-w,u-w,a+x $@

demo-stop: $(TEMPLATE_DEMOSTOP)
	if test -f $@; then chmod u+w $@; fi
	$(edit) $< > $@
	chmod g-w,u-w,a+x $@

%:	%.in
	if test -f $@; then chmod u+w $@; fi
	$(edit) $< > $@
	chmod g-w,u-w $@

clean:
	if test -n "$(GENERATED_PLATFORMS)"; then rm -f $(GENERATED_PLATFORMS); fi
	if test -n "$(GENERATED_EVENTDAEMONS)"; then rm -f $(GENERATED_EVENTDAEMONS); fi
	if test -n "$(GENERATED_GPSDLOCATIONAGENTS)"; then rm -f $(GENERATED_GPSDLOCATIONAGENTS); fi
	if test -n "$(GENERATED_MGENINPUTS)"; then rm -f $(GENERATED_MGENINPUTS); fi
	if test -n "$(GENERATED_ROUTINGCONFS)"; then rm -f $(GENERATED_ROUTINGCONFS); fi
	if test -n "$(GENERATED_EXTRA)"; then rm -f $(GENERATED_EXTRA); fi
	if test -n "$(GENERATED_OTESTPOINTDS)"; then rm -f $(GENERATED_OTESTPOINTDS); fi
	if test -n "$(GENERATED_OTESTPOINTRECORDERS)"; then rm -f $(GENERATED_OTESTPOINTRECORDERS); fi
	rm -f transportdaemon[0-9]*.xml
	rm -f .*-dep*
	rm -rf .emanegentransportxml
	rm -rf persist
	rm -f demo-start
	rm -f demo-stop
	$(MAKE) clean-local

clean-local:
