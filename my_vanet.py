#!/usr/bin/python

'Simple idea around Vehicular Ad Hoc Networks - VANETs'
'akram'
import sys
from random import randint

from mininet.node import DefaultController, RemoteController
from mininet.log import setLogLevel, info
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi
from mn_wifi.link import wmediumd, adhoc
from mn_wifi.wmediumdConnector import interference


def topology(args):
    "Create a network."
    net = Mininet_wifi(controller=DefaultController, roads=10,
                       link=wmediumd, wmediumd_mode=interference)

    info("*** Creating nodes\n")

    for id in range(0, 10):
        min_ = randint(1, 4)
        max_ = randint(11, 30)
        net.addCar('car%s' % (id+1), wlans=2, min_speed=min_, max_speed=max_)

    kwargs = {'ssid': 'vanet-ssid', 'mode': 'g', 'passwd': '123456789a',
              'encrypt': 'wpa2', 'failMode': 'standalone', 'datapath': 'user'}

    rsu11 = net.addAccessPoint(
        'RSU11', ssid='RSU11', mode='g', position='2600,3500,0', proto='batmand', channel='1')
    rsu12 = net.addAccessPoint(
        'RSU12', ssid='RSU12', mode='g', position='2800,3500,0', proto='batmand', channel='6')
    rsu13 = net.addAccessPoint(
        'RSU13', ssid='RSU13', mode='g', position='3000,3500,0', proto='batmand', channel='11')
    rsu14 = net.addAccessPoint(
        'RSU14', ssid='RSU14', mode='g', position='3200,3500,0', proto='batmand', channel='11')
    c1 = net.addController('c1')
    # c1 = net.addController(name='c1',
    #                       controller=RemoteController,
    #                       ip='192.168.8.105',
    #                       protocol='tcp',
    #                       port=6633)
    #                       ip='localhost',
    #                       protocol='tcp',
    #                      port=6653)

    info("*** Configuring Propagation Model\n")
    net.setPropagationModel(model="logDistance", exp=4)

    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()

    info("*** Associating and Creating links\n")
    net.addLink(rsu11, rsu12, proto='batmand')
    net.addLink(rsu11, rsu13, proto='batmand')
    net.addLink(rsu11, rsu14, proto='batmand')

    protocols = ['babel', 'batman_adv', 'batmand', 'olsrd', 'olsrd2']
    kwargs = dict()
    for proto in args:
        if proto in protocols:
            kwargs['proto'] = proto

    for car in net.cars:
        """net.addLink(car, intf='%s-wlan1' % car,
                    cls=mesh, ssid='mesh-ssid', channel=5)
        net.addLink(car, intf=car.wintfs[1].name,
                    cls=ITSLink, band=20, channel=181)
        net.addLink(car, intf='%s-wlan1' % car, cls=adhoc,
                    ssid='adhocNet', proto='babel', mode='g', channel=5,
                    ht_cap='HT40+', **kwargs)"""
        net.addLink(car, cls=adhoc, intf='%s-wlan0' % car,
                    ssid='adhocNet', proto='batmand', mode='g', channel=5,
                    ht_cap='HT40+', **kwargs)

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

    for id, car in enumerate(net.cars):
        car.setIP('192.168.0.%s/24' % (id+1), intf='%s-wlan0' % car)
        car.setIP('192.168.1.%s/24' % (id+1), intf='%s-wlan0' % car)
    for id, ap in enumerate(net.aps):
        ap.setIP('10.0.0.%s/24' % (id+11), intf='%s-wlan1' % ap)
        ap.setIP('10.0.1.%s/24' % (id+11), intf='%s-eth2' % ap)

    """net.cars.__getitem__(1).cmd('iperf -s -u -i 1 >> udpdownsta1exp.txt &')
    net.cars.__getitem__(2).cmd('iperf -s -u -i 1 >> udpdownsta2exp.txt &')

    net.cars.__getitem__(1).cmd(' iperf -c %s' %
                                net.cars.__getitem__(1).IP()+' -u -t 20 -b 100M >> res1.txt &')
    net.cars.__getitem__(1).cmd(' iperf -c %s' %
                                net.cars.__getitem__(2).IP()+' -u -t 20 -b 100M >> res2.txt &')"""

    info("*** Running CLI\n")
    CLI(net)

    info("*** Stopping network\n")
    net.stop()


if __name__ == '__main__':
    # setLogLevel('debug')
    topology(sys.argv)
