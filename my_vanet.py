#!/usr/bin/python


import os
import sys
import time
from random import randint

from mininet.node import Controller, RemoteController
from mininet.log import setLogLevel, info
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi
from mn_wifi.link import wmediumd, adhoc
from mn_wifi.wmediumdConnector import interference
import itertools

c2_latency_sdvn = 'c2_latency_sdvn.data'
c4_latency_sdvn = 'c4_latency_sdvn.data'

c2_latency_adhoc = 'c2_latency_adhoc.data'
c4_latency_adhoc = 'c4_latency_adhoc.data'


c2c4_iperf_sdvn = 'c2c4_iperf_sdvn.data'
c4c2_iperf_sdvn = 'c4c2_iperf_sdvn.data'

c2c4_iperf_adhoc = 'c2c4_iperf_adhoc.data'
c4c2_iperf_adhoc = 'c4c2_iperf_adhoc.data'


def apply_experiment(car):

    time.sleep(60)
    print("Applying tests for SDVN")

    # car2-car4 latency
    car[1].cmd('ping 192.168.0.4  -c 35 >> %s &' % c2_latency_sdvn)
    time.sleep(60)
    car[3].cmd('ping 192.168.0.2  -c 35 >> %s &' % c4_latency_sdvn)
    time.sleep(60)
    # car2-car4 iperf
    car[3].cmd('iperf -s -u -i 1 >> %s &' % c2c4_iperf_sdvn)
    car[1].cmd('iperf -c 192.168.0.4 -u -i 1 -t 20')
    time.sleep(30)
    # car4-car2 iperf
    car[1].cmd('iperf -s -u -i 1 >> %s &' % c4c2_iperf_sdvn)
    car[3].cmd('iperf -c 192.168.0.2 -u -i 1 -t 20')
    time.sleep(30)
    print("Applying tests for adhoc")
    # car2-car4 latency adhoc
    car[1].cmd('ping 192.168.1.4  -c 35 >> %s &' % c2_latency_adhoc)
    time.sleep(60)
    car[3].cmd('ping 192.168.1.2  -c 35 >> %s &' % c4_latency_adhoc)
    time.sleep(60)
    # car2-car4 iperf
    car[3].cmd('iperf -s -u -i 1 >> %s &' % c2c4_iperf_adhoc)
    car[1].cmd('iperf -c 192.168.1.4 -u -i 1 -t 20')
    time.sleep(30)
    # car4-car2 iperf
    car[1].cmd('iperf -s -u -i 1 >> %s &' % c4c2_iperf_adhoc)
    car[3].cmd('iperf -c 192.168.1.2 -u -i 1 -t 20')
    # time.sleep(30)


def topology(args):
    "Create a network."
    net = Mininet_wifi(controller=Controller, roads=9,
                       link=wmediumd, wmediumd_mode=interference)

    carr = []
    cars_number = 15  # { 06,10,15,20,30}
    info("*** Creating nodes\n")
    for id in range(0, cars_number):
        carr.append(id)
    info("*** Creating nodes\n")
    for id in range(0, cars_number):
        min_ = 1
        max_ = 10  # [1-10] => 3.6-36 km/s ///// [20-30] => 72-108 km/s
        carr[id] = net.addCar('car%s' % (id+1), wlans=2,
                              min_speed=min_, max_speed=max_)

    rsu11 = net.addAccessPoint(
        'RSU11', ssid='vanet-ssid', mode='g', channel='1', range=400)
    rsu12 = net.addAccessPoint(
        'RSU12', ssid='vanet-ssid', mode='g', channel='6', range=400)
    rsu13 = net.addAccessPoint(
        'RSU13', ssid='vanet-ssid', mode='g', channel='11', range=400)
    rsu14 = net.addAccessPoint(
        'RSU14', ssid='vanet-ssid', mode='g', channel='1', range=400)
    rsu15 = net.addAccessPoint(
        'RSU15', ssid='vanet-ssid', mode='g', channel='6', range=400)
    c1 = net.addController('c1')  # standard controller
    '''c1 = net.addController(name='c1',
                           controller=RemoteController,
                           ip='192.168.43.251',
                           protocol='tcp',
                           port=6653)'''
    # remote controller: opendaylight = localhost + 6633 //// floodlight= ip + 6653
    info("*** Configuring Propagation Model\n")
    net.setPropagationModel(model="logDistance", exp=4)

    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()
    info("*** Associating and Creating links\n")
    net.addLink(rsu11, rsu12)
    net.addLink(rsu11, rsu13)
    net.addLink(rsu11, rsu14)
    net.addLink(rsu11, rsu15)
    for car in net.cars:
        net.addLink(car, intf='%s-wlan1' % car,
                    cls=adhoc, proto='babel', ssid='adhocNet', mode='g')  # batman_adv babel batmand

    # draw the plotgraph
    if '-p' not in args:
        net.plotGraph(max_x=500, max_y=500)
    net.startMobility(time=0)

    info("*** Starting network\n")
    net.build()
    c1.start()
    rsu11.start([c1])
    rsu12.start([c1])
    rsu13.start([c1])
    rsu14.start([c1])
    rsu15.start([c1])

    for id, car in enumerate(net.cars):
        car.setIP('192.168.0.%s/24' % (id+1), intf='%s-wlan0' % car)
        car.setIP('192.168.1.%s/24' % (id+1), intf='%s-wlan1' % car)

    # it is better to use xterm & live testing
    # apply_experiment(carr)
    info("*** Running CLI\n")
    CLI(net)

    info("*** Stopping network\n")
    net.stop()


if __name__ == '__main__':
    # setLogLevel('debug')
    topology(sys.argv)
