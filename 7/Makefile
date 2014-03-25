TOP_DIR=..

TEMPLATE_ROUTING=routing.conf.template

NODE_COUNT=10

DEMO_ID=7

NEM_XML=

PLATFORMS=                        \
 platform.xml                     \

GENERATED_EVENTDAEMONS=           \

GENERATED_GPSDLOCATIONAGENTS=     \

GENERATED_MGENINPUTS=

GENERATED_ROUTINGCONFS=           \
 routing1.conf                    \
 routing2.conf                    \
 routing3.conf                    \
 routing4.conf                    \
 routing5.conf                    \
 routing6.conf                    \
 routing7.conf                    \
 routing8.conf                    \
 routing9.conf                    \
 routing10.conf                   


include ../rules.mk

all-local: 
	@if test -f transportdaemon1.xml; then	mv -f transportdaemon1.xml transportdaemon.xml; fi

clean-local:
	rm -f transportdaemon.xml
