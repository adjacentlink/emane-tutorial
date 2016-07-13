TOP_DIR=..

NODE_COUNT=7

DEMO_ID=2

NEM_XML=

PLATFORMS=platform.xml

GENERATED_PLATFORMS=             

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
 routing7.conf

GENERATED_OTESTPOINTDS=

GENERATED_OTESTPOINTRECORDERS=

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
 host-otestpoint-recorder1.xml \
 host-otestpoint-recorder2.xml \
 host-otestpoint-recorder3.xml \
 host-otestpoint-recorder4.xml \
 host-otestpoint-recorder5.xml \
 host-otestpoint-recorder6.xml \
 host-otestpoint-recorder7.xml \
 host-otestpoint-recorder8.xml \
 host-otestpoint-recorder9.xml \
 probe-emane-physicallayer1.xml \
 probe-emane-physicallayer2.xml \
 probe-emane-physicallayer3.xml \
 probe-emane-physicallayer4.xml \
 probe-emane-physicallayer5.xml \
 probe-emane-physicallayer6.xml \
 probe-emane-physicallayer7.xml \
 probe-emane-physicallayer8.xml \
 probe-emane-physicallayer9.xml \
 probe-emane-rfpipe1.xml \
 probe-emane-rfpipe2.xml \
 probe-emane-rfpipe3.xml \
 probe-emane-rfpipe4.xml \
 probe-emane-rfpipe5.xml \
 probe-emane-rfpipe6.xml \
 probe-emane-rfpipe7.xml \
 probe-emane-rfpipe8.xml \
 probe-emane-rfpipe9.xml

host-otestpointd%.xml: otestpointd.xml.template
	sed -e 's|@NEMID[@]|$*|g' $< > $@

host-otestpoint-recorder%.xml: otestpoint-recorder.xml.template
	sed -e 's|@NEMID[@]|$*|g' $< > $@

probe-emane-physicallayer%.xml: probe-emane-physicallayer.xml.template
	sed -e 's|@NEMID[@]|$*|g' $< > $@

probe-emane-rfpipe%.xml: probe-emane-rfpipe.xml.template
	sed -e 's|@NEMID[@]|$*|g' $< > $@

include ../rules.mk

