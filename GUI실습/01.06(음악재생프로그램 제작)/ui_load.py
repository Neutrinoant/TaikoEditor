import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import *
import pyglet
pyglet.lib.load_library('./dll/avbin')
pyglet.have_avbin=True


form_class = uic.loadUiType("./window_01_06.ui")[0]

class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.fname = ""
        self.player = pyglet.media.Player()
        self.push_load.clicked.connect(self.push_load_clicked)
        self.push_play.clicked.connect(self.push_play_clicked)
        self.push_pause.clicked.connect(self.push_pause_clicked)
        self.push_stop.clicked.connect(self.push_stop_clicked)

    def push_load_clicked(self):
        self.fname = QFileDialog.getOpenFileName(self)
        if self.fname[0] == "": # if canceled
            return  
        try:
            source = pyglet.media.load(self.fname[0])
            self.player.next_source()
            self.player.queue(source)
            self.label_songName.setText(self.fname[0].split('/')[-1])
        except:
            self.label_songName.setText('사용할 수 없는 파일 형식입니다')

    def push_play_clicked(self):
        try:
            self.player.play()
            self.label_songStatus.setText('재생중')
        except:
            self.label_songStatus.setText('재생할 수 없습니다')

    def push_stop_clicked(self):
        try:
            self.player.pause()
            self.player.seek(0)
            self.label_songStatus.setText('중지됨')
        except:
            self.label_songStatus.setText('중지할 수 없습니다')

    def push_pause_clicked(self):
        try:
            self.player.pause()
            self.label_songStatus.setText('일시정지됨')
        except:
            self.label_songStatus.setText('일시정지할 수 없습니다')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()