import serial
from serial.tools import list_ports
import sys
import threading
import math
from enum import Enum


# 受信データ種類の列挙型
class ReadTypes(Enum):
    Acceleration = 0
    Temperature = 1
    Gyroscope = 2
    Geomagnetism = 3
    Angle = 4
    Duty = 5
    IsStop = 6
    IsCurve = 7
    IsSlope = 8
    ElapsedTime = 9
    MicrocomputerBatteryVoltage = 10
    MotorBatteryVoltage = 11
    TimeStamp = 12


# 座標の列挙型
class Axis(Enum):
    X = 0
    Y = 1
    Z = 2


# 送信データ種類の列挙型
class SendTypes(Enum):
    Duty = 0
    GreenLED = 1
    RedLED = 2
    GreenLED_Flash = 3
    RedLED_Flash = 4
    AngleFinalize = 5


# ユーティリティ
class Util():

    # シリアル通信可能なポート一覧取得メソッド
    @staticmethod
    def getPortList():
        ports = list_ports.comports()
        devices = [info.device for info in ports]
        return devices

    # シリアル通信接続メソッド
    # name=ポート名
    @staticmethod
    def connectSerial(name):
        serialObj = serial.Serial(name, 115200, timeout=100)
        return serialObj

    # シリアル通信切断メソッド
    # serialObj=シリアル通信のインスタンス
    @staticmethod
    def disConnectSerial(serialObj):
        if not (serialObj is None):
            serialObj.close()

    # 受信データの整合性チェックメソッド
    # 受信データのバイト列
    @staticmethod
    def isCorrectRead(byte_s):
        return (byte_s[0] == 0xFF and
                byte_s[1] == 0xFF and
                byte_s[2] == 0x52 and
                byte_s[3] == 0x54 and
                byte_s[4] == 0x34 and
                byte_s[5] == 0x57 and
                byte_s[6] == 0x00)

    # シリアル通信データ送信メソッド
    # serialObj=シリアル通信のインスタンス
    # id=送信データ種類の列挙型
    # param=送信データのバイト 可変長引数なので2バイト目以降は引数に追加すれば送信可
    @staticmethod
    def sendParam(serialObj, id, *param):
        sendLength = 10
        if not (serialObj is None):
            send = bytearray(sendLength)
            send[0] = 99
            send[1] = 109
            send[2] = 100
            send[3] = id.value
            index = 4
            for para in param:
                send[index] = para
                index += 1
            serialObj.write(send)

    # 受信データのバイト連結メソッド 符号あり
    @staticmethod
    def joint2byte(low, high):
        con = low + (high << 8)
        if con > 32767:
            con -= 65536
        return con

    # 受信データのバイト連結メソッド 符号なし
    @staticmethod
    def joint2byte_u(low, high):
        con = low + (high << 8)
        return con

    # 受信データの値を単位計算して文字列で返すメソッド　座標無し
    # type=受信データ種類の列挙型
    # args=バイト列
    @staticmethod
    def unitChange(type, args):
        return str(Util.UnitChange[type](args))

    # 受信データの値を単位計算して文字列で返すメソッド　座標有り
    # type=受信データ種類の列挙型
    # axis=座標の列挙型
    # args=バイト列
    @staticmethod
    def unitChangeAxis(type, axis, args):
        return str(Util.UnitChange[type](axis, args))

    # 受信データの値を単位計算してそのまま返すメソッド　座標無し
    # type=受信データ種類の列挙型
    # args=バイト列
    @staticmethod
    def unitChangeRaw(type, args):
        try:
            data = Util.UnitChange[type](args)
        except:
            print("ERROR:指定された列挙型に対応するデータがバイト列から見つかりませんでした。\n座標有りの関数を使用してみてください。")
        return data

    # 受信データの値を単位計算してそのまま返すメソッド　座標有り
    # type=受信データ種類の列挙型
    # axis=座標の列挙型
    # args=バイト列
    @staticmethod
    def unitChangeAxisRaw(type, axis, args):
        try:
            data = Util.UnitChange[type](axis, args)
        except:
            print("ERROR:指定された列挙型に対応するデータがバイト列から見つかりませんでした。\n座標無しの関数を使用してみてください。")
        return data

    UnitChange = {
        ReadTypes.Acceleration: lambda axis, args: Util.joint2byte(args[0][axis.value], args[1][axis.value]) / 2048.0,
        ReadTypes.Gyroscope: lambda axis, args: Util.joint2byte(args[0][axis.value], args[1][axis.value]) / 16.4,
        ReadTypes.Geomagnetism: lambda axis, args: Util.joint2byte(args[0][axis.value], args[1][axis.value]) * 0.3,
        ReadTypes.Temperature: lambda args: Util.joint2byte(args[0], args[1]) / 340 + 35.0,
        ReadTypes.Angle: lambda args: Util.joint2byte(args[0], args[1]) * 2 * math.pi / 32767.0,
        ReadTypes.Duty: lambda args: Util.joint2byte(args[0], args[1]) / 32767 * 100,
        ReadTypes.ElapsedTime: lambda args: args[3] + (args[2] << 8) + (args[1] << 16) + (args[0] << 24),
        ReadTypes.MotorBatteryVoltage: lambda args: Util.joint2byte_u(args[0], args[1]) / 13107.0,
        ReadTypes.MicrocomputerBatteryVoltage: lambda args: Util.joint2byte_u(args[0], args[1]) / 13107.0,
        ReadTypes.IsStop: lambda args: args,
        ReadTypes.IsCurve: lambda args: args,
        ReadTypes.IsSlope: lambda args: args,
        ReadTypes.TimeStamp: lambda args: (args[3] + (args[2] << 8) + (args[1] << 16) + (args[0] << 24)) - args[4],
    }
