#! /usr/bin/env python
# coding:utf-8

import socket

import os
import struct
from ctypes import *

# host to listen on
HOST = "0.0.0.0"
PORT  = 9999 

class IP(Structure):
    _fields_ = [
            # ビットフィールドを4に設定
            ("ihl",             c_ubyte, 4),
            # ビットフィールドを4に設定
            ("version",         c_ubyte, 4),
            ("tos",             c_ubyte),
            ("len",             c_ushort),
            ("id",              c_ushort),
            ("offset",          c_ushort),
            ("ttl",             c_ubyte),
            ("protocol_num",    c_ubyte),
            ("sum",             c_ushort),
            ("src",             c_int),
            ("dst",             c_int)
            ]

    def __new__(self, socket_buffer=None):
        return self.from_buffer_copy(socket_buffer)

    def __init__(self, socket_buffer=None):
        # map protocol constants to their names
        self.protocol_map = {1:"ICMP", 6:"TCP", 17:"UDP"}

        # human readable IP adresses
        self.src_address = socket.inet_ntoa(struct.pack("<i", self.src))
        self.dst_adress = socket.inet_ntoa(struct.pack("<i", self.dst))

        # human readable protocol
        try:
            self.protocol = self.protocol_map[self.protocol_num]
        except :
            self.protocol = str(self.protocol_num)


def main():
    print "[*] start main."
    # creae a raw socket and bind it to the public interface
    socket_protocol = socket.IPPROTO_ICMP

    sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)

    sniffer.bind((HOST, PORT))
    # we want the IP headers included in the capture
    sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

    try:
        while True:
            # read in a packet
            raw_buffer = sniffer.recvfrom(65565)[0]

            # create a IP header from the first 20 bytes of the buffer
            ip_header = IP(raw_buffer[0:20])

            # print out the protocol that was detected and the hosts
            print "Protocol: %s %s -> %s" % (ip_header.protocol, ip_header.src_address, ip_header.dst_adress)

    except ValueError as e:
        print "[*]Exception Exiting."
        print str(e)

if __name__ == "__main__":
    main()
