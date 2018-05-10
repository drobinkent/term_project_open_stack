#!/bin/bash



sudo sctl -w net.ipv6.conf.all.disable_ipv6=1
sudo sysctl -w net.ipv6.conf.default.disable_ipv6=1
sudo apt-get update 
sudo apt-get install  openvswitch-* -y 
sudo ovs-vsctl add-br br0
sudo ovs-vsctl set bridge br0 protocols=OpenFlow15
sudo ovs-vsctl set controller br0 connection-mode=out-of-band
sudo ovs-vsctl add-port br0 ens4
#sudo ovs-vsctl set-manager tcp:6640
sudo ifconfig ens4 0.0.0.0
sudo dhclient br0
sudo ovs-vsctl set-controller br0 tcp:172.16.254.161:6633