TOP_DIR=..

DEMO_ID=0

NEM_XML=bypassnem.xml

GENERATED_PLATFORMS=             \
 platform1.xml                   \
 platform2.xml                   

GENERATED_EVENTDAEMONS=          \
 eventdaemon1.xml                \
 eventdaemon2.xml                

GENERATED_GPSDLOCATIONAGENTS=    \
 gpsdlocationagent1.xml          \
 gpsdlocationagent2.xml          

GENERATED_MGENINPUTS=

GENERATED_ROUTINGCONFS=           \
 routing1.conf                    \
 routing2.conf                    

NO-%:
	touch $@

GENERATED_EXTRA=           \
 NO-host-emaneeventservice \
 NO-node-emane             \
 NO-node-emaneeventd       \
 NO-node-emanetransportd   \
 NO-node-gpsd              \
 NO-node-routing

include ../rules.mk


