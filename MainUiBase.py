import threading
from UIUtil import *
from ConnectWindow import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


# メインUIのベース 継承元:UIUtil
class MainUiBase(UIUtil):
    connectFlag = False
    dutyValue = 0
    connectTimeStamp = 0

    # コンストラクタ
    def __init__(self, titleText, width, height):
        super().__init__(titleText, width, height)

    # UI関係の初期化　
    def initUI(self):
        super().initUI()
        self.__label_init()
        self.__drawControlButton()
        self.__drawInfoMonitor()
        # self.__drawSlider()
        self.__drawButton()

    # ラベルの初期化
    def __label_init(self):
        self.acc = [QLabel(), QLabel(), QLabel()]
        self.mag = [QLabel(), QLabel(), QLabel()]
        self.gyro = [QLabel(), QLabel(), QLabel()]
        self.temp = QLabel()
        self.time = QLabel()
        self.connecttime = QLabel()
        self.ang = QLabel()
        self.duty = QLabel()
        self.motorV = QLabel()
        self.microcomputerV = QLabel()
        self.stop = QLabel()
        self.curve = QLabel()
        self.slop = QLabel()

        self.labels = (self.acc, self.temp, self.gyro, self.mag, self.ang,
                       self.duty, self.stop, self.curve, self.slop, self.time,
                       self.microcomputerV, self.motorV, self.connecttime)

    # 接続・切断ボタン関係
    def __drawControlButton(self):
        buttonbox = QGridLayout()
        connectButton = QPushButton("接続", self)
        connectButton.clicked.connect(self.__showConnectWindow)
        buttonbox.addWidget(connectButton, 0, 0)
        disConnectButton = QPushButton("切断", self)
        disConnectButton.clicked.connect(self.closeConnect)
        buttonbox.addWidget(disConnectButton, 0, 1)
        self.baseLayout.addLayout(buttonbox)

    # Dutyのスライダー関係
    def __drawSlider(self):
        sliderLayout = QFormLayout()
        slider = QSlider(Qt.Horizontal, self)
        slider.setMaximum(100)
        slider.setMinimum(-100)
        sliderLabel = QLabel("Duty比:")
        sliderLayout.addRow(sliderLabel, slider)
        self.baseLayout.addLayout(sliderLayout)

    # 各種センサーなど受信データの表示関係
    def __drawInfoMonitor(self):
        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        top = QFormLayout()
        vboxLeft = QFormLayout()
        vboxRight = QFormLayout()
        formLayout = QFormLayout()
        stateLayout = QGridLayout()
        top.addRow(QLabel("ミニ四駆マイコンの実行経過時間："), self.time)
        top.addRow(QLabel("ミニ四駆マイコンの接続経過時間："), self.connecttime)
        vbox.addLayout(top)
        vboxLeft.addRow(QLabel("加速度X[g]："), self.acc[0])
        vboxLeft.addRow(QLabel("加速度Y[g]："), self.acc[1])
        vboxLeft.addRow(QLabel("加速度Z[g]："), self.acc[2])
        vboxLeft.addRow(QLabel("地磁気X[μT]]："), self.mag[0])
        vboxLeft.addRow(QLabel("地磁気Y[μT]："), self.mag[1])
        vboxLeft.addRow(QLabel("地磁気Z[μT]："), self.mag[2])
        hbox.addLayout(vboxLeft)
        vboxRight.addRow(QLabel("角速度X[deg/sec]："), self.gyro[0])
        vboxRight.addRow(QLabel("角速度Y[deg/sec]："), self.gyro[1])
        vboxRight.addRow(QLabel("角速度Z[deg/sec]："), self.gyro[2])
        vboxRight.addRow(QLabel("温度[℃]："), self.temp)
        vboxRight.addRow(QLabel("車体角度[rad]："), self.ang)
        vboxRight.addRow(QLabel("Duty比[%]："), self.duty)
        hbox.addLayout(vboxRight)
        vbox.addLayout(hbox)
        stateLayout.addWidget(QLabel("車体ステータス状況"), 0, 1)
        stateLayout.addWidget(self.stop, 1, 0)
        stateLayout.addWidget(self.curve, 1, 1)
        stateLayout.addWidget(self.slop, 1, 2)
        vbox.addLayout(stateLayout)
        formLayout.addRow(QLabel("モーター用電池電圧[V]:"), self.motorV)
        formLayout.addRow(QLabel("マイコン用電池電圧[V]:"), self.microcomputerV)
        vbox.addLayout(formLayout)
        self.baseLayout.addLayout(vbox)

    # Dutyコントロールボタン関係
    def __drawButton(self):
        buttonbox = QGridLayout()

        dutyMaxButton = QPushButton("Duty比100%", self)
        dutyMaxButton.clicked.connect(self.dutyMax)
        buttonbox.addWidget(dutyMaxButton, 2, 0)

        dutyMinButton = QPushButton("Duty比0%", self)
        dutyMinButton.clicked.connect(self.dutyMin)
        buttonbox.addWidget(dutyMinButton, 2, 1)

        dutyHalfButton = QPushButton("Duty比50%", self)
        dutyHalfButton.clicked.connect(self.dutyHalf)
        buttonbox.addWidget(dutyHalfButton, 2, 2)

        duty1UpButton = QPushButton("Duty比+1%", self)
        duty1UpButton.clicked.connect(self.duty1Up)
        buttonbox.addWidget(duty1UpButton, 1, 1)

        duty1DownButton = QPushButton("Duty比-1%", self)
        duty1DownButton.clicked.connect(self.duty1Down)
        buttonbox.addWidget(duty1DownButton, 3, 1)

        logStartButton = QPushButton("ログ記録開始", self)
        logStartButton.clicked.connect(self.startLog)
        buttonbox.addWidget(logStartButton, 4, 0)

        logStopButton = QPushButton("ログ記録終了", self)
        logStopButton.clicked.connect(self.stopLog)
        buttonbox.addWidget(logStopButton, 4, 2)

        self.baseLayout.addLayout(buttonbox)

    def dutyMax(self):
        self.dutyValue = 100
        self.sendDuty(100)

    def dutyMin(self):
        self.dutyValue = 0
        self.sendDuty(0)

    def dutyHalf(self):
        self.dutyValue = 50
        self.sendDuty(50)

    def duty1Up(self):
        self.dutyValue += 1
        self.sendDuty(self.dutyValue)

    def duty1Down(self):
        self.dutyValue -= 1
        self.sendDuty(self.dutyValue)

    def sendDuty(self, duty):
        if self.connectFlag:
            self.myThread.dutySend(duty)

    def startLog(self):
        return

    def stopLog(self):
        return

    def __showConnectWindow(self):
        connectWindow = ConnectWindow(self)
        connectWindow.show()

    def closeConnect(self):
        if self.connectFlag:
            self.connectTimeStamp = 0
            self.myThread.closeConnect()
            self.connectFlag = False

    def connectSerial(self, name):
        self.myThread = SerialThread(name)
        self.myThread.read.connect(self.readEvent)
        self.myThread.error.connect(self.errorEvent)
        self.myThread.connected.connect(self.connectedEvent)
        self.myThread.start()

    # エラーイベント　シリアル通信時にエラーが起きたら呼ばれりゅ
    def errorEvent(self, para):
        self.connectTimeStamp = 0
        QMessageBox.critical(
            None, "エラー", "シリアル通信に失敗しました。\n\n" + para, QMessageBox.Ok)

    # データ受信イベント　データ受信時に呼ばれる
    def readEvent(self, byte_s):
        if (Util.isCorrectRead(byte_s)):
            self.byteDetas = [[[byte_s[8], byte_s[10], byte_s[12]],
                               [byte_s[9], byte_s[11], byte_s[13]]],
                              [byte_s[14], byte_s[15]],
                              [[byte_s[16], byte_s[18], byte_s[20]],
                               [byte_s[17], byte_s[19], byte_s[21]]],
                              [[byte_s[22], byte_s[24], byte_s[26]],
                               [byte_s[23], byte_s[25], byte_s[27]]],
                              [byte_s[28], byte_s[29]],
                              [byte_s[30], byte_s[31]],
                              byte_s[32],
                              byte_s[33],
                              byte_s[34],
                              [byte_s[38], byte_s[37], byte_s[36], byte_s[35]],
                              [byte_s[39], byte_s[40]],
                              [byte_s[41], byte_s[42]],
                              [byte_s[38], byte_s[37], byte_s[36], byte_s[35], self.connectTimeStamp]]

            elapsedTime = self.getData(ReadTypes.ElapsedTime)
            if (self.connectTimeStamp >= elapsedTime or self.connectTimeStamp == 0):
                self.connectTimeStamp = elapsedTime

            with open('log.csv', 'a') as f:
                print(self.changeTextAxis(ReadTypes.Acceleration, Axis.X),
                      self.changeTextAxis(ReadTypes.Acceleration, Axis.Y),
                      self.changeTextAxis(ReadTypes.Acceleration, Axis.Z),
                      self.changeTextAxis(ReadTypes.Geomagnetism, Axis.X),
                      self.changeTextAxis(ReadTypes.Geomagnetism, Axis.Y),
                      self.changeTextAxis(ReadTypes.Geomagnetism, Axis.Z),
                      self.changeTextAxis(ReadTypes.Gyroscope, Axis.X),
                      self.changeTextAxis(ReadTypes.Gyroscope, Axis.Y),
                      self.changeTextAxis(ReadTypes.Gyroscope, Axis.Z),
                      self.changeText(ReadTypes.Temperature),
                      self.changeText(ReadTypes.Angle),
                      self.changeText(ReadTypes.Duty),
                      self.changeText(ReadTypes.MotorBatteryVoltage),
                      self.changeText(ReadTypes.MicrocomputerBatteryVoltage),
                      self.changeText(ReadTypes.ElapsedTime),
                      self.changeText(ReadTypes.IsStop),
                      self.changeText(ReadTypes.IsCurve),
                      self.changeText(ReadTypes.IsSlope),
                      self.changeText(ReadTypes.TimeStamp), sep=",", file=f)

    # 受信データの値を単位計算してそのまま返す関数　座標無し
    # type=受信データ種類の列挙型
    def getData(self, types):
        index = types.value
        para = self.byteDetas[index]
        return Util.unitChangeRaw(types, para)

    # 受信データの値を単位計算してそのまま返す関数　座標有り
    # type=受信データ種類の列挙型
    # axis=座標の列挙型
    def getAxisData(self, types, axis):
        index = types.value
        para = self.byteDetas[index]
        return Util.unitChangeAxisRaw(types, axis, para)

    def changeText(self, types):
        index = types.value
        para = self.byteDetas[index]
        self.labels[types.value].setText(Util.unitChange(types, para))
        return Util.unitChangeRaw(types, para)

    def changeTextAxis(self, types, axis):
        index = types.value
        axisIndex = axis.value
        para = self.byteDetas[index]
        self.labels[index][axisIndex].setText(
            Util.unitChangeAxis(types, axis, para))
        return Util.unitChangeAxisRaw(types, axis, para)

    # ログ出力関数　タイムスタンプを自動付加　引数:表示させたい内容
    def logPrint(self, text):
        timestanp = self.getData(ReadTypes.TimeStamp)
        elapsedtime = self.getData(ReadTypes.ElapsedTime)
        output = "timestanp = {timestanp} / elapsedtime = {elapsedtime} / text = {text}".format(
            timestanp=timestanp, elapsedtime=elapsedtime, text=text)
        print(output)

    # 接続完了イベント
    def connectedEvent(self):
        self.connectFlag = True


# シリアル通信実行スレッド
class SerialThread(QThread):
    read = pyqtSignal(bytes)
    error = pyqtSignal(str)
    connected = pyqtSignal()
    flag = True
    readLength = 43

    # コンストラクタ
    def __init__(self, portName, parent=None):
        super().__init__(parent=parent)
        self.name = portName

    # スレッド実行部分
    def run(self):
        try:
            self.serialObj = Util.connectSerial(self.name)
            self.connected.emit()
            while self.flag:
                self.read.emit(self.serialObj.read(self.readLength))
                QThread.msleep(50)

        except SerialException as e:
            self.error.emit(str(e))

    # duty送信関数 引数:duty
    def dutySend(self, duty):
        if (duty < 0):
            duty += 65535
        duty_L = duty & 0x000000ff
        duty_H = (duty & 0x0000ff00) >> 8
        Util.sendParam(self.serialObj, SendTypes.Duty, duty_H, duty_L)

    # シリアル通信切断関数
    def closeConnect(self):
        self.flag = False
        Util.disConnectSerial(self.serialObj)
