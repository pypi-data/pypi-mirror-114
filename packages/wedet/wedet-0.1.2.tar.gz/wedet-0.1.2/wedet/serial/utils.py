#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Time    : 2021-7-3 15:14:05
# @Email   : jariof@foxmail.com

import time
import serial
import logging


class SerialUtils:
    def __init__(self, port, baudrate=115200, timeout=5):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.com = None
        self.last_bytes = bytearray()

    def com_open(self):
        """
        串口的的打开；
        :return: 返回串口的句柄；
        """
        try:
            self.com = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
            logging.debug('Open Serial: {}'.format(self.port))
        except Exception as msg:
            logging.error('open port:{}, baudrate:{} error occur'.format(self.port, self.baudrate))
            logging.error(msg)

    def com_close(self):
        """
        串口的关闭；
        :return:None;
        """
        if self.com is not None and self.com.isOpen:
            logging.info('Close Serial: {}'.format(self.port))
            self.com.close()

    def com_send_data(self, data, use_bytes=False):
        """
        向打开的端口发送数据；
        :param data: 发送的数据信息；
        :param use_bytes: 是否直接传入字节；
        :return: 发送的数据内容的长度；
        """
        if self.com is None:
            self.com_open()
        if use_bytes:
            success_bytes = self.com.write(data)
        else:
            success_bytes = self.com.write(data.encode('UTF-8'))
        return success_bytes

    def com_get_data(self, timeout=5, use_bytes=False):
        """
        通过串口获取数据，默认等待时间为5s，
        :param timeout: 读取数据的超时时间，默认值为5；
        :param use_bytes: 是否直接接收字节；
        :return: 获取串口返回的数据；
        """
        if use_bytes:
            all_data = bytearray()
        else:
            all_data = ''
        if self.com is None:
            self.com_open()
        start_time = time.time()
        while True:
            end_time = time.time()
            if end_time - start_time < timeout:
                len_data = self.com.inWaiting()
                if len_data != 0:
                    for i in range(1, len_data + 1):
                        data = self.com.read(1)
                        if use_bytes:
                            all_data.extend(data)
                        else:
                            data = data.decode('utf-8')
                            all_data = all_data + data
                        if i == len_data:
                            break
                else:
                    logging.debug('Received data is null')
            else:
                break
        logging.debug('Received data:{}'.format(all_data))
        return all_data

    def com_get_data_by_header_length(self, header, length):
        """
        通过串口获取数据，获得头为header，长度为length的数据
        :param header: 拟提取头；
        :param length: 数据长度；
        :return: 获取串口返回的数据；
        """
        loading_data = bytearray()
        all_data = bytearray()
        all_data.extend(self.last_bytes)

        if self.com is None:
            self.com_open()

        loading = True
        while loading:
            len_data = self.com.inWaiting()
            if len_data != 0:
                for i in range(1, len_data + 1):
                    data = self.com.read(1)
                    all_data.extend(data)
                    if i == len_data:
                        break
                if len(all_data) >= length:
                    for i in range(len(all_data) - (len(header)-1)):
                        congruence = True
                        for j in range(len(header)):
                            if all_data[i+j] != header[j]:
                                congruence = False
                        if congruence and len(all_data)-i >= length:
                            loading_data = all_data[i:i+length]
                            self.last_bytes = all_data[length:]
                            # print(len(self.last_bytes))
                            loading = False
            else:
                logging.debug('Received data is null')

        logging.debug('Received data:{}'.format(loading_data))
        return loading_data


class ComAP(SerialUtils):
    def __init__(self, port, baudrate=115200, timeout=5):
        super().__init__(port, baudrate, timeout)

    def com_ap_open(self):
        """
        打开串口的方法；
        :return：返回当前串口句柄；
        """
        self.com_open()

    def com_ap_close(self):
        """
        关闭串口；
        :return:None；
        """
        self.com_close()

    def com_ap_send_data(self, data, default_char='\r'):
        """
        向串口发送指定字符串，默认发送完最后加回车；
        :param data: 发送的命令；
        :param default_char: 发送的命令后添加的默认回车字符；
        :return:发送的字符长度；
        """
        self.com_send_data(data + default_char)

    def com_ap_get_data(self, timeout=2):
        """
        从串口读取数据，默认在等待时间后读取的数据返回；
        :param timeout:默认值为2s;
        :return: 串口返回的数据；
        """
        return self.com_get_data(timeout)
