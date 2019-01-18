import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *  # for QPixmap

main_class = uic.loadUiType("./ProjectTaiko/window_01_09.ui")[0]

class MainWindow(QMainWindow, main_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.spin_mupper.valueChanged.connect(self.measureChanged)
        self.combo_mlower.currentTextChanged.connect(self.measureChanged)

    def measureChanged(self):
        self.label_measure.setText('MEASURE '+str(self.spin_mupper.value())+'/'+self.combo_mlower.currentText())
      
if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MainWindow()
    myWindow.show()
    app.exec_()