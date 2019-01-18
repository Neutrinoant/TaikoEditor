import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import *

form_class = uic.loadUiType("C:/Users/Anty/Documents/Python Scripts/ProjectTaiko/window_01_05.ui")[0] #, resource_suffix="C:/Users/Anty/Documents/Python Scripts/ProjectTaiko/music")[0]

class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        self.quitButton.clicked.connect(QCoreApplication.instance().quit) # use quit method from 'app' var.
        self.playButton.clicked.connect(self.btn_play_clicked)
        self.pauseButton.clicked.connect(self.btn_pause_clicked)
        self.stopButton.clicked.connect(self.btn_stop_clicked)

        self.lineEdit_songName.textChanged.connect(self.lineEdit_song_changed)
        self.lineEdit_songName.returnPressed.connect(self.lineEdit_song_entered)

        self.msg_radio = "안들음"
        self.radio_yes.clicked.connect(self.radio_clicked)
        self.radio_no.clicked.connect(self.radio_clicked)

        self.msg_check = "음악"
        self.check_peace.stateChanged.connect(self.check_state)
        self.check_sad.stateChanged.connect(self.check_state)
        self.check_strange.stateChanged.connect(self.check_state)
        self.check_angry.stateChanged.connect(self.check_state)

        self.msg_completeness = 0
        self.msg_score = 0.0
        self.spin_completeness.valueChanged.connect(self.spin_score_changed)
        self.doubleSpin_score.valueChanged.connect(self.spin_score_changed)
        

    def btn_play_clicked(self):
        self.label_songStatus.setText("재생중")

    def btn_pause_clicked(self):
        QMessageBox.about(self, 'message', self.label_songStatus.text())
        self.label_songStatus.setText("일시정지")

    def btn_stop_clicked(self):
        self.label_songStatus.clear()

    def lineEdit_song_changed(self):
        self.label_songName.setText(self.lineEdit_songName.text())

    def lineEdit_song_entered(self):
        self.status_message()

    def radio_clicked(self):
        if self.radio_yes.isChecked():
            self.msg_radio = '들었음'
        elif self.radio_no.isChecked():
            self.msg_radio = '안들음'
        else:
            self.msg_radio = ""
        self.status_message()

    def check_state(self):
        self.msg_check = ""
        if self.check_peace.isChecked():
            self.msg_check += "평화 "
        if self.check_sad.isChecked():
            self.msg_check += "슬픔 "
        if self.check_strange.isChecked():
            self.msg_check += "기괴 "
        if self.check_angry.isChecked():
            self.msg_check += "분노 "
        self.msg_check += "음악"
        self.status_message()

    def spin_score_changed(self):
        self.msg_completeness = self.spin_completeness.value()
        self.msg_score = self.doubleSpin_score.value()
        self.status_message()

    def status_message(self):
        text = '현재곡'
        text += '('+self.msg_radio+')'
        text += ': '
        text += self.lineEdit_songName.text()
        text += ' ['+self.msg_check+']'
        text += ' [완성도 '+str(self.msg_completeness)+' / 평점 '+str(self.msg_score)+']'
        self.statusbar.showMessage(text)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()