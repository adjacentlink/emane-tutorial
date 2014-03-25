TOP_DIR=..

DEMO_ID=4

NEM_XML=ieee80211abgnem.xml

PLATFORMS=                      \
 platform1.xml                  \
 platform2.xml                  \
 platform3.xml                  \
 platform4.xml                  

GENERATED_EVENTDAEMONS=         \

GENERATED_GPSDLOCATIONAGENTS=    

GENERATED_MGENINPUTS=

GENERATED_ROUTINGCONFS=          

GENERATED_EXTRA=     \
 node-preapplication

include ../rules.mk

node-preapplication:
	echo -e "#!/bin/bash -\nifconfig emane0 txqueuelen 8192\n" > $@
	chmod 755 $@
