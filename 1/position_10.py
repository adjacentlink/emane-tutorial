#!/usr/bin/env python
try:
    from emane.events import EventService
    from emane.events import LocationEvent
except:
    from emanesh.events import EventService
    from emanesh.events import LocationEvent

# create the event service
service = EventService(('224.1.2.8',45703,'emanenode0'))

# create an event setting 10's position
event = LocationEvent()
event.append(10,latitude=40.031290,longitude=-74.523095,altitude=3.000000)

# publish the event
service.publish(0,event)

