import serial
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from MainUi import *


# メイン
def main():
    app = QApplication(sys.argv)
    ui = MainUi("ミニ四駆コントローラ", 400, 300)
    ui.showUI()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
