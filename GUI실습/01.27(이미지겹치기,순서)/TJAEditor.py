import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import bisect
import random
import copy

form_class = uic.loadUiType("mainWindow.ui")[0]

class MainWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        self.donIndex_list = []
        self.don_list = []
        self.MAX_WIDTH = self.label_beat.width()

        self.push_changeOrder.clicked.connect(self.push_changeOrder_clicked)
        self.push_add.clicked.connect(self.push_add_clicked)
        self.push_del.clicked.connect(self.push_del_clicked)

    def push_changeOrder_clicked(self):
        self.label_don3.raise_()
        self.label_don3.stackUnder(self.label_don2)

    def makeLabelDon(self):
        # make label_don
        donImage = QPixmap(':/res/res/note/img_don.png')
        label = QLabel(self.centralWidget())
        label.setPixmap(donImage)
        label.setGeometry(QRect(0,0,0,0))
        label.setScaledContents(True)
        return label

    def push_add_clicked(self):
        if len(self.donIndex_list) > self.MAX_WIDTH//10:
            return
        while True:
            i = random.randrange(0, self.MAX_WIDTH, step=10)
            if i not in self.donIndex_list:
                break

        # make new img_don
        newLabel = self.makeLabelDon()
        imgW, imgH = self.label_beat.height()//3, self.label_beat.height()//3
        imgX, imgY = self.label_beat.pos().x()+i-imgW//2, \
                    self.label_beat.pos().y()+self.label_beat.height()//2-imgH//2
        newLabel.setGeometry(QRect(imgX, imgY, imgW, imgH))
        newLabel.setObjectName('label_don_'+str(i))

        # insert new img_don in sorted list
        donIndex = bisect.bisect_left(self.donIndex_list, i)
        self.donIndex_list.insert(donIndex, i)
        self.don_list.insert(donIndex, newLabel)

        # set z-value of new img_don
        newLabel.raise_()
        if donIndex > 0:
            newLabel.stackUnder(self.don_list[donIndex-1])
        newLabel.show()

    def push_del_clicked(self):
        if not self.donIndex_list:
            return
        i = random.randrange(0, len(self.donIndex_list))
        self.donIndex_list.pop(i)
        self.don_list.pop(i).deleteLater()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MainWindow()
    myWindow.show()
    app.exec_()