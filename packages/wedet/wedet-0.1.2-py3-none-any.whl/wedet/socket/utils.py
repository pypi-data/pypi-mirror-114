#!/usr/bin/env python3
# -*- coding:utf-8 -*-


def make_crc_table():
    poly = 0x8408
    table = []
    for byte in range(256):
        crc = 0
        for bit in range(8):
            if (byte ^ crc) & 1:
                crc = (crc >> 1) ^ poly
            else:
                crc >>= 1
            byte >>= 1
        table.append(crc)
    return table


crc_table = make_crc_table()


def crc_16_fast(msg):
    crc = 0xffff
    for byte in msg:
        crc = crc_table[(byte ^ crc) & 0xff] ^ (crc >> 8)
    crc = crc ^ 0xffff
    hi, lo = crc >> 8, crc & 0xff
    return bytes([hi, lo])
