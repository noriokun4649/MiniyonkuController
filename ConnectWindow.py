from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from Util import *
from serial.serialutil import SerialException


class ConnectWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.w = QDialog(parent)
        self.w.setWindowTitle("接続")
        layout = QFormLayout()
        self.combo = QComboBox()
        self.combo.addItems(Util.getPortList())
        layout.addRow(QLabel("接続先ポート："), self.combo)
        buttonConnect = QPushButton("接続")
        buttonConnect.clicked.connect(self.connectSerialSub)
        buttonCancel = QPushButton("キャンセル")
        buttonCancel.clicked.connect(self.w.close)

        layout.addRow(buttonConnect, buttonCancel)
        self.w.setLayout(layout)

    def connectSerialSub(self):
        name = self.combo.currentText()
        self.parent.connectSerial(name)
        self.w.close()

    def show(self):
        self.w.exec_()
