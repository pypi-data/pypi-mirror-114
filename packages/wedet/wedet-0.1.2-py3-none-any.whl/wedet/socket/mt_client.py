#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import socket
import struct
from wedet.socket.mt_server import check_crc_nx, DetDataNX
import time


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 9093))
last_data = b''

t1 = time.time()
cnt = 0
tt = 0.
while True:
    data = last_data + s.recv(1024)
    _l = len(data)
    for i in range(_l - 1):
        if b'\xEA\x9B' == data[i: i+2]:
            if _l >= i+6:
                n_bytes = struct.unpack('i', data[i+2: i+6])[0]
                # print(n_bytes)
                if _l >= i+n_bytes:
                    msg = data[i: i+n_bytes]
                    last_data = data[i+n_bytes:]
                    if check_crc_nx(msg):
                        nx_data = DetDataNX()
                        nx_data.unpack(msg)
                        # print(nx_data)
                        dt = time.time() - t1
                        cnt += 1
                        tt += dt
                        if tt >= 1.:
                            print("FPS: {}".format(cnt))
                            cnt = 0
                            tt = 0.
                        t1 = time.time()
                else:
                    last_data = data[i:]
            else:
                last_data = data[i:]
