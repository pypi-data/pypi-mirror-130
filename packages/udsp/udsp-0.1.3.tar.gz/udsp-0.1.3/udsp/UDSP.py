from udsp.ARXTD import *
from udsp.DSP import *
import serial
import time


class UDSP:  # serial DSP
    def __init__(self, port, cb, baudrate=115200, txsize=100):
        self.alive = True
        self.txbuf = bytearray(txsize)

        self.ser = serial.Serial(port, baudrate, timeout=0.5)

        self.arxtd = ARXTD(self.ser.read_all, b'\r\n', b'')
        self.dsp = DSP(self.txbuf, bytearray(1), cb)

    def Retribute(self, new_buf):
        self.dsp.rxbuf = new_buf
        self.dsp.RxReset()

    def Cmd(self, v):
        self.dsp.TxReset()
        self.dsp.cmd = v

    def Decode(self):
        self.arxtd.Update()
        while len(self.arxtd):
            self.Retribute(self.arxtd.Pop())
            self.dsp.Decode()

    def Encode(self, fmt, *data):
        self.dsp.Encode(fmt, *data)

        def Send(self):

            self.ser.write(bytes(self.dsp.txbuf) + b'\r\n')


if __name__ == "__main__":
    def func(cmd, ds):
        if cmd == 1:
            print(ds.O('B'))


    sdsp = SDSP("COM29", func)
    sdsp.Encode('BBB', 1, 1, 1)  # 选择B1
    sdsp.Cmd(1)  # 为输出
    sdsp.Send()
    while True:
        # sdsp.Decode()
        sdsp.Encode('BBB', 1, 1, 1)  # 选择B1
        sdsp.Cmd(3)  # 拉高
        sdsp.Send()
        time.sleep(1)
        sdsp.Encode('BBB', 1, 1, 1)  # 选择B1
        sdsp.Cmd(4)  # 拉低
        sdsp.Send()
        time.sleep(1)
        # print(tmp)
