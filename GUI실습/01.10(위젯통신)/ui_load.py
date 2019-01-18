import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic

main_class = uic.loadUiType("./ProjectTaiko/window_01_10.ui")[0]

class MainWindow(QMainWindow, main_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.push_userInput.clicked.connect(self.push_userInput_clicked)

    def push_userInput_clicked(self):
        dlg = MessageDialog()
        print(dlg.exec_())
        self.label_message.setText(dlg.lineEdit_message.text())


message_class = uic.loadUiType("./ProjectTaiko/dialog_01_10.ui")[0]

class MessageDialog(QDialog, message_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.push_OK.clicked.connect(self.push_OK_clicked)

    def push_OK_clicked(self):
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()