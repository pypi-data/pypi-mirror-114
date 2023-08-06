#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import socket
import threading
import time
import struct
import logging
from typing import List
from wedet.socket.utils import crc_16_fast


class BoxNX:
    """
    NX端 目标外包框
    Float (x1, y1, x2, y2).
    """

    def __init__(self, x1: float = 0, y1: float = 0, x2: float = 0, y2: float = 0,
                 track_id: int = -1, score: float = 1.):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.track_id = track_id
        self.score = score
        self.bytes_len = 24

    def pack(self):
        box_packed = struct.pack('ffffif', self.x1, self.y1, self.x2, self.y2, self.track_id, self.score)
        return box_packed

    def unpack(self, box_bytes):
        assert isinstance(box_bytes, bytes) and len(box_bytes) == self.bytes_len, \
            'box_bytes should be bytes and length={}'.format(self.bytes_len)
        self.x1, self.y1, self.x2, self.y2, self.track_id, self.score = struct.unpack('ffffif', box_bytes)

    def __len__(self):
        return self.bytes_len

    def __str__(self):
        return 'box: [{:.3f}, {:.3f}, {:.3f}, {:.3f}], track_id: {}, score: {:.3f}'.format(
            self.x1, self.y1, self.x2, self.y2, self.track_id, self.score)


class DetDataNX:
    """
    NX端 目标检测结果数据结构
    """

    def __init__(self, image_w: int = 0, image_h: int = 0):
        """
        Args:
            image_w: int 检测图像的像素宽度
            image_h: int 高度
        """
        self.image_w = image_w
        self.image_h = image_h
        self.box_list = []

    def pack(self, box_list: List[BoxNX]):
        self.box_list = box_list
        _header = b'\xEA\x9B'
        _len = 2 + 4
        _wh = struct.pack('ii', self.image_w, self.image_h)
        _len += 8
        _boxes = b''
        for b in box_list:
            _boxes += b.pack()
            _len += len(b)
        _len += 2
        _bytes_len = struct.pack('i', _len)
        _msg = _header + _bytes_len + _wh + _boxes
        _crc = crc_16_fast(_msg)
        _msg += _crc
        return _msg

    def unpack(self, msg_bytes: bytes):
        assert b'\xEA\x9B' == msg_bytes[0: 2], "msg header WRONG (!= 0xEA 0x9B)"
        _len = struct.unpack('i', msg_bytes[2: 6])[0]
        assert len(msg_bytes) == _len, "msg length WRONG"
        self.image_w, self.image_h = struct.unpack('ii', msg_bytes[6: 14])
        self.box_list = []
        for i in range(14, _len-2, 24):
            b = BoxNX()
            b.unpack(msg_bytes[i: i+24])
            self.box_list.append(b)

    def __str__(self):
        _s = 'image_w: {}, image_h: {}\n'.format(self.image_w, self.image_h)
        for i in range(len(self.box_list)):
            _s += '  - {}\n'.format(self.box_list[i])
        return _s


def check_crc_nx(msg: bytes):
    crc_recv = msg[-2:]
    crc_calc = crc_16_fast(msg[:-2])
    return crc_calc == crc_recv


mutex = threading.Lock()


class MTSocketServer(threading.Thread):

    def __init__(self, port=9000):
        threading.Thread.__init__(self)
        socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        socket_server.bind(('', port))
        socket_server.listen(5)
        print('Start listening on port {} ...'.format(port))
        self.socket_server = socket_server
        self.listening = True
        self.connected_clients = dict()

    def quit(self):
        for k, c in self.connected_clients.items():
            c.close()
        self.listening = False

    def run(self):
        while self.listening:
            client_socket, client_address = self.socket_server.accept()
            client_key = '{}:{}'.format(client_address[0], client_address[1])
            print('Got client: [{}]'.format(client_key))

            self.connected_clients[client_key] = client_socket
            """
            non_keeps = []
            for k, c in self.connected_clients.items():
                try:
                    mutex.acquire()
                    print('key: {}, send: {}'.format(k, c.send(b'\xEA\x9A')))
                    mutex.release()
                except socket.error as e:
                    print('key: {}, send: error'.format(k))
                    c.close()
                    non_keeps.append(k)
            for k in non_keeps:
                del self.connected_clients[k]
            """
            # print(' --- {}'.format(self.connected_clients))

    def send_detections(self, box_list: List[BoxNX], image_w: int, image_h: int):
        nx_data = DetDataNX(image_w, image_h)
        msg = nx_data.pack(box_list)
        non_keeps = []
        for k, c in self.connected_clients.items():
            try:
                c.send(msg)
            except socket.error as e:
                print('key: {}, send: error'.format(k))
                c.close()
                non_keeps.append(k)
        for k in non_keeps:
            del self.connected_clients[k]


if __name__ == '__main__':
    box1 = BoxNX(10, 109, 1060, 1000, track_id=-1, score=1.)
    box2 = BoxNX(12, 108, 1050, 1100, track_id=-1, score=1.)
    box3 = BoxNX(13, 107, 1040, 1200, track_id=-1, score=1.)
    box4 = BoxNX(14, 106, 1030, 1300, track_id=-1, score=1.)
    data = DetDataNX(1920, 1080)
    msg = data.pack([box1, box2, box3, box4])
    print(data)
    if check_crc_nx(msg):
        data2 = DetDataNX()
        data2.unpack(msg)
        print(data2)

    server = MTSocketServer(9093)
    server.start()

    frame = 0
    while True:
        time.sleep(0.001)
        frame += 1
        server.send_detections([box1, box2, box3, box4], 1920, 1080)
        print('send {}'.format(str(frame).zfill(6)))

    server.join()
