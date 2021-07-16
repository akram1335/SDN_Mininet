#!/usr/bin/python

'Simple idea around Vehicular Ad Hoc Networks - VANETs'
import os
import sys
import time
'''import matplotlib
matplotlib.use('TkAgg')'''
import matplotlib.pyplot as plt
from random import randint

from mininet.node import Controller, RemoteController
from mininet.log import setLogLevel, info
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi
from mn_wifi.link import wmediumd, mesh, adhoc
from mn_wifi.wmediumdConnector import interference
import itertools

# Store metrics here
c0_throughput0 = 'c0_throughput0.data'          # car0 throughput phase 1
client_throughput0 = 'client_throughput0.data'	# client throughput phase 1

c0_latency0 = 'c0_latency0.data'		# car0 latency phase 1
c3_latency0 = 'c3_latency0.data'		# car3 latency phase 1

c0c3_iperf0 = 'c0c3_iperf0.data'            # car0-car3 phase 1
c3client_iperf0 = 'c3client_iperf0.data'	# car3-client phase 1

# Implement the graphic function in order to demonstrate the network measurements
def graphic():
    #plt.clf()	# clear current figure
    #plt.ioff()
    # Throughput
    # open "client_throughputX.data" file in current directory, in read mode - store lines in variable
    f1 = open('./' + 'client_throughput0.data', 'r')	
    f1_lines = f1.readlines()
    f1.close()

    # open "c0_throughput.data" file - store lines in variable
    f2 = open('./' + 'c0_throughput0.data', 'r')
    f2_lines = f2.readlines()
    f2.close()

    rx = []
    d_rx = []
    tx = []
    d_tx = []
    time_rx = []
    time_tx = []

    i = 0
    num = 0
    # read line by line
    for x in f1_lines:    
        if num % 2 == 0:
            p = x.split()	    # p: list of all the words in each line, seperation by space
            print(str(p[0])+ " = " + str(p[4]))
                                # RX bytes: total bytes received through the interface
                            	# take all words in 2nd element of p, seperated by :
            rx.append(int(p[4]))# fill rx with the 2nd element of the 2nd element of p
            if len(rx) > 1:
                d_rx.append(rx[i] - rx[i - 1])	#store the differences between subsequent rxes, in d_rx
            i += 1
        num += 1

    i = 0
    num = 0
    # read line by line
    for x in f2_lines:    
        if num % 2 != 0:
            p = x.split()
            print(str(p[0])+ " = " + str(p[4]))
                                # TX bytes: total bytes transmitted through the interface
                                # take all words in 6th element of p, seperated by :
            tx.append(int(p[4]))# fill tx with the 2nd element of the 6th element of p
            if len(tx) > 1:
                d_tx.append(tx[i] - tx[i - 1])	#store the differences between subsequent txes, in d_tx
            i += 1
        num += 1

    # create time axes
    i = 0
    for x in range(len(d_tx)):    
        time_tx.append(i)
        i = i + 0.5

    i = 0
    for x in range(len(d_rx)):    
        time_rx.append(i)
        i = i + 0.5
    
    '''print ("aaaaaaaa")
    fig = plt.figure(figsize=(16,6))    # start a figure
    print ("bbbbbbb")
    g = fig.add_subplot(121)            # addtime a 1st subfigure
    print ("cccccc")
    print(str(time_rx)+ " = =" + str(d_rx))
    g.plot(time_rx, d_rx)
    print ("ddddddd")				
    plt.xlabel('Time')
    plt.ylabel('Bytes')
    print ("eeeeee")
    plt.ylim([-100, 100000])
    #plt.ylim([-100, 1000])
    print ("ffffff")
    plt.title('Client - RX')

    print ("1111111")
    b = fig.add_subplot(122)		    # add a 2nd subfigure
    print ("222222")
    b.plot(time_tx, d_tx)
    print ("333333")
    plt.xlabel('Time')
    plt.ylabel('Bytes')
    print ("4444444")
    plt.ylim([-100, 100000])
    #plt.ylim([-100, 1000])
    print ("5555555")
    plt.title('Car0 - TX')
    print ("666666")
    plt.savefig('Plot_Throughput_phase0.png')
    print ("77777777")
    #plt.close(fig)
    print ("ttttttt")
    plt.clf()
    print ("99999999")'''

    print ("aaaaaaaa")
    fig = plt.figure(figsize=(16,6))
    print ("+++++")
    plt.plot(time_rx, d_rx)
    print ("bbbbbb")
    plt.xlabel('Seconds')
    plt.ylabel('Sent Data(Bytes)')
    plt.title('Difference between packets sent by car 0')
    savename='Plot_Throughput_phase0.png'
    print ("cccccccc")
    plt.savefig(savename)
    print ("ddddddddd")
    #plt.clf()
    #plt.close(fig)
    fig1 = plt.figure(figsize=(16,6))
    print ("eeeeeeeee")
    plt.plot(time_tx, d_tx)
    print ("fffffff")
    plt.xlabel('Seconds')
    plt.ylabel('Sent Data(Bytes)')
    plt.title('Packets sent by car 0')
    savename='Plot_Throughput_phase0please.png'
    print ("jjjj")
    plt.savefig(savename)
    print ("hhhhhh")
    plt.close(fig1)
    #plt.clf()
    print ("iiiiii")
    # Latency
    f1 = open('./' + 'c0_latency0.data', 'r')
    f1_lines = f1.readlines()
    f1.close()
    print ("88888888")
    lat = []
    time = []
    i = 1
    fl =  len(f1_lines) - 5
    while i <= fl:  
        x = f1_lines[i]  
        p = x.split()
        t = p[6].split('=')
        lat.append(float(t[1]))
        i = i +1   
    print ("jjjjj")
    # calculations for phase 1
    f2 = open('./' + 'c3_latency0.data', 'r')
    f2_lines = f2.readlines()
    f2.close()
    lat2 = []
    i = 1
    fl2 =  len(f2_lines) - 5
    while i <= fl2:  
        x = f2_lines[i]  
        p = x.split()
        t = p[6].split('=')
        lat2.append(float(t[1]))
        i = i + 1
    total = []
    total = [sum(i) for i in zip(lat,lat2)]
    i = 1
    for x in range(len(total)):    
        time.append(i)
        i = i + 1
    
    print ("101010101010")
    fig2 = plt.figure(figsize=(16,6))
    print ("eeeeeeeee")
    plt.plot(time,total)
    print ("jjjjjj")
    plt.xlabel('Time (ms)')
    print ("kkkk")
    plt.ylabel('Ping number')
    print ("ssss")
    plt.savefig('Plot_Latency_phase0.png')
    print ("hhhhhhhh")
    plt.close(fig2)
    #plt.clf()
    print ("1212121212")
       

    # Jitter and Packet Loss
    for j in range(0,1):
        time_jitter = []
        time_loss = []
        jitter = []
        loss =[]
        		# calculations for phase 1
        f1 = open('./' + c0c3_iperf0 , 'r')
        f1_lines = f1.readlines()
        f1.close()
        f2 = open('./' + c3client_iperf0, 'r')
        f2_lines = f2.readlines()
        f2.close()
        i = 7
        while i < len(f1_lines):
            x = f1_lines[i] 
            p = x.split()
            l = len(p)
            if l > 12:
                t = p[l-1].split('%')
                t2 = t[0].split('(')
                loss.append(float(t2[1]))
                jitter.append(float(p[l-5]))
            i = i +1
        jitter1 = []
        loss1 = []
        i = 7
        while i < len(f2_lines):
            x = f2_lines[i] 
            p = x.split()
            l = len(p)
            if l > 12:
                t = p[l-1].split('%')
                t2 = t[0].split('(')
                loss1.append(float(t2[1]))
                jitter1.append(float(p[l-5]))
            i = i +1
        total_jitter = []
        total_loss = []
        total_jitter = [sum(i) for i in zip(jitter,jitter1)]
        total_loss = [sum(i) for i in zip(loss,loss1)]
        i = 1
        for x in range(len(total_loss)):    
            time_loss.append(i)
            i = i + 1
        i = 1
        for x in range(len(total_jitter)):    
            time_jitter.append(i)
            i = i + 1
        print ("13131313")
        fig3 = plt.figure(figsize=(16,6))
        print ("212151616416518498465")
        plt.plot(time_jitter,total_jitter)
        plt.xlabel('Iperf number')
        plt.ylabel('Jitter (ms)')
        plt.savefig('Plot_Jitter_phase0.png')
        plt.close(fig3)
        #plt.clf()
        fig4 = plt.figure(figsize=(16,6))
        print ("1411414414")
        plt.plot(time_loss,total_loss)
        plt.xlabel('Iperf number')
        plt.ylabel('Packet Loss (%)')
        plt.savefig('Plot_PacketLoss_phase0.png')
        plt.close(fig4)
        #plt.clf()
    
    print ("ready")

def apply_experiment(car,client):
    
    taskTime = 20

    time.sleep(12)
    print ("Applying first phase")

    # car0-car3 latency
    car[1].cmd('ping 192.168.0.4  -c 20 >> %s &' % c0_latency0)	# latency phase 1
    car[3].cmd('ping 192.168.0.9  -c 20 >> %s &' % c3_latency0)	

    # car0-car3 iperf
    car[3].cmd('iperf -s -u -i 1 >> %s &' % c0c3_iperf0)        # iperf metrics phase 1
    car[1].cmd('iperf -c 192.168.0.4 -u -i 1 -t 20')
    time.sleep(25)
    # car3-client iperf
    client.cmd('iperf -s -u -i 1 >> %s &' % c3client_iperf0)	#-s: iperf in server mode, -u=use UDP not TCP 
    car[3].cmd('iperf -c 192.168.0.9 -u -i 1 -t 20')		        #-i interval=1, -t=transmit for 20 sec, to client
                                                                #-c: accept connections only to this host
    # car0-client throughput
    timeout = time.time() + taskTime
    currentTime = time.time()
    i = 0
    while True:
        if time.time() > timeout:
            break;
        if time.time() - currentTime >= i:		# store RX and TX data phase 1
            car[1].cmd('ifconfig car2-wlan0 | grep \"bytes\" >> %s' % c0_throughput0)
            client.cmd('ifconfig car9-wlan0 | grep \"bytes\" >> %s' % client_throughput0)
            i += 0.5
    
    

    #time.sleep(2)
    



def topology(args):
    "Create a network."
    net = Mininet_wifi(controller=RemoteController, roads=10,
                       link=wmediumd, wmediumd_mode=interference)

    carr = []
    info("*** Creating nodes\n")
    for id in range(0, 10):
        carr.append(id)

    for id in range(0, 10):
        min_ = randint(1, 4)
        # max_ = randint(11, 30)
        max_ = randint(11, 20)
        # net.addCar('car%s' % (id+1), wlans=2, min_speed=min_, max_speed=max_)
        carr[id] = net.addCar('car%s' % (id+1), wlans=2, ip='10.0.0.%s/8' % (id+1),
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

    # c1 = net.addController('c1')
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

    # ///////////////////////////////////////////////////////////////////////////
    '''
    carr[1].cmdPrint(
        "vlc -vvv bunnyMob.mp4 --sout '#duplicate{dst=rtp{dst=192.168.0.9,port=5004,mux=ts},dst=display}' :sout-keep &")
    carr[8].cmdPrint("vlc rtp://@192.168.0.9:5004 &")'''
    print("before sleep")
    time.sleep(20)
    print("after sleep")
    apply_experiment(carr, carr[8])

    # Uncomment the line below to generate the graph that you implemented
    graphic()

    # kills all the xterms that have been opened
    print ("1111")
    os.system('pkill xterm')
    print ("222")
    # ///////////////////////////////////////////////////////////////////////////
    info("*** Running CLI\n")
    CLI(net)
    print ("333")
    info("*** Stopping network\n")
    net.stop()
    print ("444")


if __name__ == '__main__':
    # setLogLevel('debug')
    # setLogLevel('info')
    try:
        topology(sys.argv)
        print ("555")
    except:
        print ("topology failed...")
