from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from ConnectWindow import *


class UIUtil(QWidget):

    # コンストラクタ
    def __init__(self, titleText, width, height):
        super().__init__()
        self.marginLeft = 20
        self.marginTop = 20
        self.width = width
        self.height = height
        self.title = titleText
        self.baseLayout = self.layoutBaseSetting()
        self.initUI()

    # UI関係の初期化
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setLayout(self.baseLayout)
        self.setGeometry(self.marginLeft, self.marginTop,
                         self.width, self.height)

    # UIの表示
    def showUI(self):
        self.show()

    # ベースレイアウト
    def layoutBaseSetting(self):
        layout = QVBoxLayout()
        return layout
