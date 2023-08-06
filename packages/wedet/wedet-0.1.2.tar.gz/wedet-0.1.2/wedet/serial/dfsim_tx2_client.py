#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Time    : 2021-7-3 15:14:05
# @Email   : jariof@foxmail.com

from ctypes import c_short, c_uint, c_int, c_long, c_float, c_double
import struct
import time
import threading
from .utils import SerialUtils


class SimDataTx2:
    """
    Tx2端发送数据结构
    """
    def __init__(self):
        self.dict_data = dict()
        self.dict_data['uHeader'] = b"\xEA\x9B"
        self.dict_data['uId'] = b"\x11"
        self.dict_data['uCount'] = b"\x00"
        self.dict_data['uCtlMode'] = b"\x02"  # 控制方式
        self.dict_data['uLongitudeinalCtlMode'] = b"\x00"  # 纵向模态控制模式
        self.dict_data['uLateralCtlMode'] = b"\x00"  # 横侧向模态控制模式
        self.dict_data['uThrottleCtlMode'] = b"\x00"  # 自动油门模态控制
        self.dict_data['fLongitudinalBar'] = struct.pack("f", 0.01)  # 纵向杆
        self.dict_data['fLateralBar'] = struct.pack("f", 0.01)  # 横向杆
        self.dict_data['fRudder'] = struct.pack("f", 0.01)  # 方向舵
        self.dict_data['fThrottle'] = struct.pack("f", 0.01)  # 油门
        # self.fSpeedReducer = 0  # 减速板
        self.dict_data['uSwitchingValue'] = b"\x00"  # 开关量
        self.dict_data['dHeightControl'] = struct.pack("d", 0.01)  # c_double(0.01)  # 高度控制
        self.dict_data['fVerticalSpeedControl'] = struct.pack("f", 0.01)  # 垂直速度控制
        self.dict_data['fPitchAttitudeControl'] = struct.pack("f", 0.01)  # 俯仰姿态控制
        self.dict_data['fPitchControl'] = struct.pack("f", 0.01)  # 航迹角控制（倾角）（预留）
        self.dict_data['fDriftControl'] = struct.pack("f", 0.01)  # 航迹角控制（偏角）（预留）
        self.dict_data['fPitchAttitudRate'] = struct.pack("f", 0.01)  # 俯仰姿态速率控制
        self.dict_data['fNormalOverloadControl'] = struct.pack("f", 0.01)  # 法向过载控制
        self.dict_data['fPitchRateControl'] = struct.pack("f", 0.01)  # 俯仰角速率控制
        self.dict_data['fRollAngleControl'] = struct.pack("f", 0.01)  # 滚转角控制
        self.dict_data['fRollRateControl'] = struct.pack("f", 0.01)  # 滚转速率控制
        self.dict_data['fYawAngleControl'] = struct.pack("f", 0.01)  # 偏航角控制
        self.dict_data['fCourseControl'] = struct.pack("f", 0.01)  # 航向控制
        self.dict_data['fAirspeedControl'] = struct.pack("f", 0.01)  # 空速控制
        self.dict_data['fThrustControl'] = struct.pack("f", 0.01)  # 推力控制
        self.dict_data['fVelNormalACC'] = struct.pack("f", 0.01)  # 速度系（x轴）法向加速度
        self.dict_data['fVelRollAngle'] = struct.pack("f", 0.01)  # 速度西法向加速度方向
        self.dict_data['fVelNormalXACC'] = struct.pack("f", 0.01)  # 速度系切向加速度
        self.dict_data['uSendComData'] = b"\x00"  # 发送给友机数据链信息
        # self.uDeviceStatus = 0  # 嵌入式设备状态
        self.dict_data['uComReSendData'] = b"\x00\x00\x00\x00\x00\x00"  # 通信预留
        self.dict_data['uChecksums'] = b"\x00"
        self.com_data = b''

    def __str__(self):
        pass

    def _concat_once(self):
        self.com_data = self.dict_data['uHeader']
        for i, v in enumerate(self.dict_data.values()):
            if i > 0:
                self.com_data += v

    def pack_me(self):
        self._concat_once()
        print("length: {}".format(len(self.com_data)))
        self.dict_data['uCount'] = bytes([len(self.com_data)])
        self._concat_once()
        return self.com_data


class SerialReader(threading.Thread):
    def __init__(self, thread_id, name, counter):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.name = name
        self.counter = counter

    def run(self):
        global g_msg
        su = SerialUtils('COM3')
        su.com_open()
        data = SimDataTx2()
        # data_bytes = data.pack_me()
        # su.com_send_data(data.pack_me(), use_bytes=True)

        t0 = time.time()
        while 1:
            t1 = time.time()
            msg = su.com_get_data_by_header_length(header=bytearray(b"\xEA\x9B"), length=102)
            print(len(msg))
            g_msg = msg
            ba = bytearray()
            ba.append(msg[81])
            ba.append(msg[80])
            ba.append(msg[79])
            ba.append(msg[78])
            ret = struct.unpack('!f', ba)[0]
            # print("msg: {}, {}, {}, {}, {}".format(ret, msg[78], msg[79], msg[80], msg[81]))
            if ret != 0.5:
                assert False, "ERROR"
            t2 = time.time()
            if t2 - t0 >= 1.:
                fps = 1. / (t2 - t1)
                # print(fps)
                t0 = time.time()


if __name__ == "__main__":
    global g_msg
    g_msg = bytearray()
    thr1 = SerialReader(1, "Thread-1", 1)

    thr1.start()
    while 1:
        time.sleep(0.1)
        ba = bytearray()
        ba.append(g_msg[81])
        ba.append(g_msg[80])
        ba.append(g_msg[79])
        ba.append(g_msg[78])
        ret = struct.unpack('!f', ba)[0]
        print("msg: {}, {}, {}, {}, {}".format(ret, g_msg[78], g_msg[79], g_msg[80], g_msg[81]))

    thr1.join()
