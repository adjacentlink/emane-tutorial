#!/usr/bin/env python
#
# Copyright (c) 2014 - Adjacent Link LLC, Bridgewater, New Jersey
# Copyright (c) 2012 - DRS CenGen, LLC, Columbia, Maryland
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# * Redistributions of source code must retain the above copyright
#   notice, this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in
#   the documentation and/or other materials provided with the
#   distribution.
# * Neither the name of DRS CenGen, LLC nor the names of its
#   contributors may be used to endorse or promote products derived
#   from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#

import pycurl
import re
import sys
import threading
import os
import time
import telnetlib
import json
from lxml import etree
from optparse import OptionParser
from pynodestatviz import NodeStatViz


usage = "%prog [OPTION]... "

optionParser = OptionParser(usage=usage)

optionParser.add_option("", 
                        "--location",
                        action="store",
                        type="string",
                        dest="locations",
                        metavar="FILE",
                        default=os.path.join(os.environ['HOME'],'.pynodestatviz-locations.xml'),
                        help="File containing initial node screen locations [default: %default]")

(options, args) = optionParser.parse_args()

if len(args) != 0 :
    print >> sys.stderr, "invalid number of arguments"
    exit(1)

class Stoppable():
    def __init__(self):
        self._running = True
        self._runningLock = threading.Lock()

    def stop(self):
        self._runningLock.acquire()
        self._running = False
        self._runningLock.release()

    def _checkRunning(self):
        self._runningLock.acquire()
        running = self._running
        self._runningLock.release()
        return running

class NodeTextInfoThread(threading.Thread,Stoppable):
    def __init__(self,nodeId,links,lock):
        threading.Thread.__init__(self)
        Stoppable.__init__(self)
        self._nodeId = nodeId
        self._links = links
        self._lock = lock

    def _processInfo(self,buf):
        self._lock.acquire()
        
        if self._nodeId not in self._links:
            self._links[self._nodeId] =  {'addr' : None}

        self._links[self._nodeId]['links'] = {}
        self._links[self._nodeId]['valid'] = True
        self._links[self._nodeId]['aka'] = []
        
        for line in buf.split("\n"):
            m = re.match("^(\d+.\d+\.\d+\.\d+)\s+(\d+.\d+\.\d+\.\d+)\s+"\
                             "(\d+\.\d+)\s+(\d+\.\d+)\s+"\
                             "(\d+\.\d+)\s+(\d+\.\d+)",line)

            if m:
                if m.group(1) not in self._links:
                    self._links[self._nodeId]['addr'] = m.group(1)

                self._links[self._nodeId]['links'][m.group(2)] = \
                    {
                    'hyst' : float(m.group(3)),
                    'lq'   : float(m.group(4)),
                    'nlq'  : float(m.group(5)),
                    'cost' : float(m.group(6)),
                    }


                self._links[self._nodeId]['addr'] =  m.group(1)
                
                if m.group(1) not in self._links[self._nodeId]['aka']:
                    self._links[self._nodeId]['aka'].append(m.group(1))

        self._lock.release()                
        

    def run(self):
        while self._checkRunning():
            c = pycurl.Curl()
            c.setopt(pycurl.CONNECTTIMEOUT, 1)
            c.setopt(pycurl.TIMEOUT, 1)
            c.setopt(pycurl.NOSIGNAL, 1)
            c.setopt(pycurl.URL, "http://node-%d:2006/links" %(self._nodeId))
            c.setopt(pycurl.WRITEFUNCTION, self._processInfo)

            try:
                c.perform()

                time.sleep(2)
            except pycurl.error, error:
                # txtinfo was resetting conneciton
                if error[0] == 56:
                    time.sleep(2)
                else:
                    self._lock.acquire()

                    if self._nodeId not in self._links:
                        self._links[self._nodeId] = {'addr': None}

                    self._links[self._nodeId]['links'] = {}
                    self._links[self._nodeId]['valid'] = False

                    self._lock.release()

                    time.sleep(1)


class NodeGPSDThread(threading.Thread,Stoppable):
    def __init__(self,nodeId,locations,lock):
        threading.Thread.__init__(self)
        Stoppable.__init__(self)
        self._nodeId = nodeId
        self._locations = locations
        self._lock = lock

    def run(self):
        while self._checkRunning():
            try:
                session = telnetlib.Telnet("node-%d"%self._nodeId,2947,5)

                session.write("?WATCH={\"enable\":true,\"json\":true}\n")

                while self._checkRunning():
                    (_,_,line) = session.expect([".+\n"])

                    # fix a json message bug in some versions of gpsd
                    line = line.replace('"parity":"}','"parity":""}')

                    data = json.loads(line.rstrip())

                    if 'lat' in data:
                        self._lock.acquire()

                        if self._nodeId not in self._locations:
                            self._locations[self._nodeId] = None

                        self._locations[self._nodeId] = (data['lat'],data['lon'],data['alt'])

                        self._lock.release()
            except:
                self._locations[self._nodeId] = None
                time.sleep(1)
             

class DisplayUpdate(threading.Thread,Stoppable):
    def __init__(self,app,links,linksLock,locations,locationsLock):
        threading.Thread.__init__(self)
        Stoppable.__init__(self)
        self._app = app
        self._links = links
        self._linksLock = linksLock
        self._locations = locations
        self._locationsLock = locationsLock

    def run(self):
        knownNodes = {}

        while self._checkRunning():
            rootElement = etree.Element("nodestatviz")
            titleElement = etree.SubElement(rootElement, 
                                            "title",
                                            text="OLSR Link Viewer with GPS Info")

            
            nodesElement = etree.SubElement(rootElement, "nodes")
            nodeInfo = {}
            foundNodes = []
            addressMap = {}

            self._linksLock.acquire()

            for node in sorted(self._links, key=self._links.get):
                foundNodes.append(node)

                if self._links[node]['addr']:
                    name = str(self._links[node]['addr'])
                else:
                    name = str(node)

                if self._links[node]['valid']:
                    color = 'green'
                else:
                    color = 'red'

                etree.SubElement(nodesElement, "node", name=name, color=color)

                nodeInfo[node] = {'valid' : self._links[node]['valid'],
                                  'links' : 0}

                if self._links[node]['addr']:
                    addressMap[self._links[node]['addr']] = node

                    for addr in self._links[node]['aka']:
                        addressMap[addr] = node

            edgesElement = etree.SubElement(rootElement, "edges")

            for node in sorted(self._links, key=self._links.get):
                for neighbor in sorted(self._links[node]['links'], key=self._links[node]['links'].get):
                    if neighbor in addressMap and self._links[node]['addr'] in addressMap:
                        lq = self._links[node]['links'][neighbor]['lq']

                        if lq >= .75:
                            color = 'black'
                        elif lq >= .5:
                            color = 'blue'
                        elif lq >=.25:
                            color = 'yellow'
                        else:
                            color = 'red'

                        if self._links[node]['addr'] in self._links[addressMap[neighbor]]['links']:
                            lq = self._links[addressMap[neighbor]]['links'][self._links[node]['addr']]['lq']

                            if lq >= .75:
                                color2 = 'black'
                            elif lq >= .5:
                                color2 = 'blue'
                            elif lq >=.25:
                                color2 = 'yellow'
                            else:
                                color2 = 'red'
                        else:
                            color2 = color

                        etree.SubElement(edgesElement,
                                         "edge",
                                         src=self._links[node]['addr'],
                                         dst=self._links[addressMap[neighbor]]['addr'],
                                         style="solid_to_dash",
                                         color=color,
                                         color2=color2)
                        
                        nodeInfo[node]['links'] += 1

            self._linksLock.release()

            tableElement = etree.SubElement(rootElement, "table")

            headerElement = etree.SubElement(tableElement, "header")

            etree.SubElement(headerElement, "column", text="Node", width="15", background="dark gray",)

            etree.SubElement(headerElement, "column", text="Links", width="5",background="dark gray")

            etree.SubElement(headerElement, "column", text="Latitude", background="dark gray")

            etree.SubElement(headerElement, "column", text="Longitude",background="dark gray")

            etree.SubElement(headerElement, "column", text="Altitude", background="dark gray")

            rowsElement = etree.SubElement(tableElement, "rows")

            for node in nodeInfo:
                if self._links[node]['addr']:
                    name = str(self._links[node]['addr'])
                else:
                    name = str(node)

                rowElement = etree.SubElement(rowsElement, "row")
                if nodeInfo[node]['valid']:
                    background = 'white'
                else:
                    background = 'red'
                    
                etree.SubElement(rowElement, "column", text=name,background=background)
                etree.SubElement(rowElement, "column", text=str(nodeInfo[node]['links']),background=background)
                
                self._locationsLock.acquire()
                lat = ""
                lon = ""
                alt = ""

                if node in self._locations:

                   pos =  self._locations[node]
                   
                   if pos:
                       if pos[0]:
                           lat = pos[0]

                       if pos[1]:
                           lon = pos[1]

                       if  pos[2]:
                           alt = pos[2]
                       
                self._locationsLock.release()                       

                etree.SubElement(rowElement, "column", text=str(lat),background=background)

                etree.SubElement(rowElement, "column", text=str(lon),background=background)

                etree.SubElement(rowElement, "column", text=str(alt),background=background)

            update=etree.tostring(rootElement,pretty_print=True)

            self._app.update(update)

            time.sleep(2)

links = {}

app = NodeStatViz(options.locations)

linksLock = threading.Lock()
threads = []

for i in range(1,11):
    t = NodeTextInfoThread(i,links,linksLock)
    t.start()
    threads.append(t)

locations = {}

locationsLock = threading.Lock()

for i in range(1,11):
    t = NodeGPSDThread(i,locations,locationsLock)
    t.start()
    threads.append(t)

displayThread = DisplayUpdate(app,links,linksLock,locations,locationsLock)

displayThread.start()
threads.append(displayThread)

app.mainloop()

for t in threads:
    t.stop()

for t in threads:
    t.join()

exit(0)



