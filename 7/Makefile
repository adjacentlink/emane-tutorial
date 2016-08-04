TOP_DIR=..

TEMPLATE_ROUTING=routing.conf.template

NODE_COUNT=10

DEMO_ID=7

NEM_XML=

PLATFORMS= \
 platform.xml

GENERATED_EVENTDAEMONS=

GENERATED_GPSDLOCATIONAGENTS=

GENERATED_MGENINPUTS=

GENERATED_ROUTINGCONFS= \
 routing1.conf \
 routing2.conf \
 routing3.conf \
 routing4.conf \
 routing5.conf \
 routing6.conf \
 routing7.conf \
 routing8.conf \
 routing9.conf \
 routing10.conf                   

GENERATED_EXTRA= \
 host-otestpointd1.xml \
 host-otestpointd2.xml \
 host-otestpointd3.xml \
 host-otestpointd4.xml \
 host-otestpointd5.xml \
 host-otestpointd6.xml \
 host-otestpointd7.xml \
 host-otestpointd8.xml \
 host-otestpointd9.xml \
 host-otestpointd10.xml \
 host-otestpoint-recorder1.xml \
 host-otestpoint-recorder2.xml \
 host-otestpoint-recorder3.xml \
 host-otestpoint-recorder4.xml \
 host-otestpoint-recorder5.xml \
 host-otestpoint-recorder6.xml \
 host-otestpoint-recorder7.xml \
 host-otestpoint-recorder8.xml \
 host-otestpoint-recorder9.xml \
 host-otestpoint-recorder10.xml \
 probe-emane-commeffect1.xml \
 probe-emane-commeffect2.xml \
 probe-emane-commeffect3.xml \
 probe-emane-commeffect4.xml \
 probe-emane-commeffect5.xml \
 probe-emane-commeffect6.xml \
 probe-emane-commeffect7.xml \
 probe-emane-commeffect8.xml \
 probe-emane-commeffect9.xml \
 probe-emane-commeffect10.xml \
 probe-emane-rawtransport1.xml \
 probe-emane-rawtransport2.xml \
 probe-emane-rawtransport3.xml \
 probe-emane-rawtransport4.xml \
 probe-emane-rawtransport5.xml \
 probe-emane-rawtransport6.xml \
 probe-emane-rawtransport7.xml \
 probe-emane-rawtransport8.xml \
 probe-emane-rawtransport9.xml \
 probe-emane-rawtransport10.xml

include ../rules.mk

#all-local: 
#	@if test -f transportdaemon1.xml; then	mv -f transportdaemon1.xml transportdaemon.xml; fi

#clean-local:
#	rm -f transportdaemon.xml

host-otestpointd%.xml: otestpointd.xml.template
	sed -e 's|@NEMID[@]|$*|g' \
		-e 's|@DISCOVERYPORT[@]|$(shell expr $(*) + 8880)|g' \
		-e 's|@PUBLISHPORT[@]|$(shell expr $(*) + 8890)|g' $< > $@

host-otestpoint-recorder%.xml: otestpoint-recorder.xml.template
	sed -e 's|@NEMID[@]|$*|g' \
		-e 's|@PUBLISHPORT[@]|$(shell expr $(*) + 8890)|g' $< > $@

probe-emane-commeffect%.xml: probe-emane-commeffect.xml.template
	sed -e 's|@NEMID[@]|$*|g' $< > $@

probe-emane-rawtransport%.xml: probe-emane-rawtransport.xml.template
	sed -e 's|@NEMID[@]|$*|g' $< > $@
