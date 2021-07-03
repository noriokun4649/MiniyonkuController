from MainUiBase import *


# メインUI　継承元:MainUiBase
class MainUi(MainUiBase):

    # コンストラクタ
    def __init__(self, titleText, width, height):
        super().__init__(titleText, width, height)

    # データ受信イベント　データ受信時に呼ばれる
    def readEvent(self, byte_s):
        super().readEvent(byte_s)
        self.sendDuty(50)
        self.logPrint("Duty比を50に設定しました！")
