#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import socket
import struct


udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.bind(('', 8080))
last_msg = b''
pkg_len = 44


def parse_wrzf_msg(wrzf_msg: bytes):
    # wrzf_msg = bytearray(wrzf_msg)
    uheader, udev, ungps, ustat, fell, fvec, falt, dlat, dlng, syear, umon, uday, \
    uhour, umin, usec, umsec, scrc, utail1,utail2 = struct.unpack('ccccfffddhcccccchcc', wrzf_msg)
    uhour, umin, usec, umsec = int.from_bytes(uhour, 'big'), int.from_bytes(umin, 'big'), \
                               int.from_bytes(usec, 'big'), int.from_bytes(umsec, 'big')
    print('alt: {:.6f}, lat: {:.6f}, lng: {:.6f}, hour: {}, min: {}, sec: {}, msec: {}'.format(
        falt, dlat, dlng, uhour, umin, usec, umsec))


while 1:
    r_msg, r_addr = udp_socket.recvfrom(1024)
    r_msg = last_msg + r_msg
    l_msg = len(r_msg)
    # print(l_msg)
    i = 0
    while i < l_msg:
        if bytes([r_msg[i]]) == b'\xFE':
            if l_msg - i >= pkg_len:
                if bytes([r_msg[i+pkg_len-2]]) == b'\x0D' and bytes([r_msg[i+pkg_len-1]]) == b'\x0A':
                    # print(r_msg[i: i+pkg_len])
                    parse_wrzf_msg(r_msg[i: i+pkg_len])
                    i += pkg_len - 1
            else:
                last_msg = r_msg[i:]
                break
        i += 1
