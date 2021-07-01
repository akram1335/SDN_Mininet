#!/usr/bin/python

'Simple idea around Vehicular Ad Hoc Networks - VANETs'

import sys
from random import randint

from mininet.node import Controller, RemoteController
from mininet.log import setLogLevel, info
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi
from mn_wifi.link import wmediumd, mesh, adhoc
from mn_wifi.wmediumdConnector import interference


def topology(args):
    "Create a network."
    net = Mininet_wifi(controller=RemoteController, roads=10,
                       link=wmediumd, wmediumd_mode=interference)

    info("*** Creating nodes\n")
    for id in range(0, 10):
        min_ = randint(1, 4)
        #max_ = randint(11, 30)
        max_ = randint(11, 20)
        #net.addCar('car%s' % (id+1), wlans=2, min_speed=min_, max_speed=max_)
        net.addCar('car%s' % (id+1), wlans=2, ip='10.0.0.%s/8' % (id+1),
                   mac='00:00:00:00:00:0%s' % id, mode='b', min_speed=min_, max_speed=max_)
    '''
    rsu11 = net.addAccessPoint('RSU11', ssid='RSU11', mode='g', channel='1')
    rsu12 = net.addAccessPoint('RSU12', ssid='RSU12', mode='g', channel='6')
    rsu13 = net.addAccessPoint('RSU13', ssid='RSU13', mode='g', channel='11')
    rsu14 = net.addAccessPoint('RSU14', ssid='RSU14', mode='g', channel='11')'''
    rsu11 = net.addAccessPoint('RSU11', ssid='RSU11', dpid='1000000000000000',
                               mode='g', channel='1', range=400)
    rsu12 = net.addAccessPoint('RSU12', ssid='RSU12', dpid='2000000000000000',
                               mode='g', channel='6', range=400)
    rsu13 = net.addAccessPoint('RSU13', ssid='RSU13', dpid='3000000000000000',
                               mode='g', channel='11', range=400)

    #c1 = net.addController('c1')
    c1 = net.addController(name='c1',
                           controller=RemoteController,
                           ip='localhost',
                           protocol='tcp',
                           port=6653)
    # port=6633)
    info("*** Configuring Propagation Model\n")
    net.setPropagationModel(model="logDistance", exp=4)

    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()

    info("*** Associating and Creating links\n")
    net.addLink(rsu11, rsu12)
    net.addLink(rsu11, rsu13)
    # net.addLink(rsu11, rsu14)//////////
    for car in net.cars:
        net.addLink(car, intf='%s-wlan1' % car,
                    cls=mesh, ssid='mesh-ssid', proto='batmand', mode='g', channel=5,
                    ht_cap='HT40+')
    if '-p' not in args:
        net.plotGraph(max_x=500, max_y=500)

    net.startMobility(time=0)

    info("*** Starting network\n")
    net.build()
    c1.start()
    rsu11.start([c1])
    rsu12.start([c1])
    rsu13.start([c1])
    # rsu14.start([c1])

    for id, car in enumerate(net.cars):
        car.setIP('192.168.0.%s/24' % (id+1), intf='%s-wlan0' % car)
        car.setIP('192.168.1.%s/24' % (id+1), intf='%s-mp1' % car)
        car.setMAC('00:00:00:00:00:0%s' % id)

    info("*** Running CLI\n")
    CLI(net)

    info("*** Stopping network\n")
    net.stop()


if __name__ == '__main__':
    # setLogLevel('debug')
    topology(sys.argv)
