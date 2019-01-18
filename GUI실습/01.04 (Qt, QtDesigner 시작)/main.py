'''
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
'''
'''
app = QApplication(sys.argv) # must be placed at this loc
label = QLabel("Hello World!")
label.show()
app.exec_()
'''
'''
app = QApplication(sys.argv) # must be placed at this loc
label = QPushButton("Hello World!")
label.show()
app.exec_()
'''
'''
class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hello!")
        self.setGeometry(300,300, 300,400) # (topleft(x,y), width, height)): x(horisontal), y(vertical)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mywindow = MyWindow()
    mywindow.show()
    app.exec_()
'''
'''
class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hello!")
        self.setGeometry(300,300, 300,400)

        btn_play = QPushButton("Play", self)
        btn_play.move(20,20) # button position (x,y)
        btn_play.clicked.connect(self.btn_play_clicked)

        btn_pause = QPushButton("Pause", self)
        btn_pause.move(20,50) # button position (x,y)
        btn_pause.clicked.connect(self.btn_pause_clicked)

        btn_stop = QPushButton("Stop", self)
        btn_stop.move(20,80) # button position (x,y)
        btn_stop.clicked.connect(self.btn_stop_clicked)

    def btn_play_clicked(self):
        QMessageBox.about(self, "message", "play?")
    
    def btn_pause_clicked(self):
        QMessageBox.about(self, "message", "pause?")

    def btn_stop_clicked(self):
        QMessageBox.about(self, "message", "stop?")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mywindow = MyWindow()
    mywindow.show()
    app.exec_()
'''