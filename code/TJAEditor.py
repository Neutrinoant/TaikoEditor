import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import bisect
import random
import copy
import Score

form_class = uic.loadUiType("mainWindow.ui")[0]

class MainWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        self.donIndex_list = []
        self.don_list = []

        self.push_changeOrder.clicked.connect(self.push_changeOrder_clicked)
        self.push_add.clicked.connect(self.push_add_clicked)
        self.push_del.clicked.connect(self.push_del_clicked)
        self.push_addBeat.clicked.connect(self.push_addBeat_clicked)
        self.push_delBeat.clicked.connect(self.push_delBeat_clicked)

        self.label_beat.setFixedSize(self.scrollArea.height()*2/3,self.scrollArea.height()*2/3)
        self.MAX_WIDTH = self.label_beat.width()

        self.beatInfo = {'beats':[], 'hIndex':-1}

        self.push_load.clicked.connect(self.push_load_clicked)
        # print(self.label_beat.width())


    def push_changeOrder_clicked(self):
        self.label_don3.raise_()
        self.label_don3.stackUnder(self.label_don2)

    def makeLabelNote(self,note):
        # make label_don
        label = NoteLabel(self.scrollAreaWidgetContents)
        if note == 0:
            pass
        elif note==1:
            noteImage= QPixmap(':/res/res/note/img_don.png')
        elif note==2:
            noteImage = QPixmap(':/res/res/note/img_kat.png')
        elif note==3:
            noteImage= QPixmap(':/res/res/note/img_don_big.png')
        elif note==4:
            noteImage= QPixmap(':/res/res/note/img_kat_big.png')
        
        if noteImage!=None:
            label.setPixmap(noteImage)
        beatSize=[self.label_beat.height(),self.label_beat.height()]
        if note==1 or note==2:
            label.setGeometry(0,0,beatSize[0]//3,beatSize[1]//3)
        else:
            label.setGeometry(0,0,beatSize[0]//2,beatSize[1]//2)
        label.setScaledContents(True)
        label.show()
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

    def push_addBeat_clicked(self):
        # make new img_beat
        beatImage = QPixmap(':/res/res/track/beat(48x50).png')
        label = ClickableLabel(self.scrollAreaWidgetContents)
        label.setBeatInfo(self.beatInfo)
        label.setPixmap(beatImage)
        label.setScaledContents(True)
        label.setFixedSize(self.scrollArea.height()*2/3, self.scrollArea.height()*2/3)
        label.lower()
        print(label.width(), label.height())

        # insert new img_beat in layout and managable list
        self.horizontalLayout.addWidget(label)
        self.beatInfo['beats'].append(label)

    def push_delBeat_clicked(self):
        # delete highlighted beat
        if self.beatInfo['hIndex'] < 0:
            return
        self.beatInfo['beats'].pop(self.beatInfo['hIndex'])
        self.horizontalLayout.takeAt(self.beatInfo['hIndex']).widget().deleteLater()
        print(self.beatInfo['hIndex'])
        self.beatInfo['hIndex'] = -1


    def push_load_clicked(self):
        fname = QFileDialog.getOpenFileName(self)[0]
        score = Score.TJA(fname)
        track = score.track_list[0]
        barIdx = 0

        for bar in track.bar_list:
            m = bar.measure
            beatList = [self.makeLabelBeat() for _ in range(m[0]-1)]
            beatList.append(self.makeLabelBeat(end=True))
            beatIdx = 0

            for beat in bar.beat_list:
                w, h = beatList[beatIdx].width(), beatList[beatIdx].height()
                numSplit = beat.splitParam
                offset = beatList[0].width() // numSplit
                noteList=list()
                for note in beat.note_list:
                    N=self.makeLabelNote(note.getNote())
                    N.setNote(note)
                    noteList.append(N)

                for i in range(len(noteList)):
                    noteList[i].move(w+(barIdx*m[0]+beatIdx)*w+offset*i-noteList[i].width()/2, self.label_beat.height()/2)  # need modify
                beatIdx += 1

            barIdx += 1

        self.score = score


            

    def makeLabelBeat(self, end=False):
        # make new img_beat
        if not end:
            beatImage = QPixmap(':/res/res/track/beat(48x50).png')
        else:
            beatImage = QPixmap(':/res/res/track/beat_end(48x50).png')
        label = QLabel(self.scrollAreaWidgetContents)
        label.setPixmap(beatImage)
        label.setScaledContents(True)
        label.setFixedSize(self.scrollArea.height()*2/3, self.scrollArea.height()*2/3)
        label.lower()
        label.show()

        # insert new img_beat in layout and managable list
        self.horizontalLayout.addWidget(label)
        # print(label.x(), label.y())
        
        # print(self.scrollAreaWidgetContents.x(), self.scrollAreaWidgetContents.y(), self.scrollAreaWidgetContents.width(), self.scrollAreaWidgetContents.height())
        return label

class NoteLabel(QLabel):
    def __init__(self,parent):
        super().__init__(parent)
        self.note=Score.Note()
    def setNote(self,Note):
        self.note.setNote(Note)



    
class ClickableLabel(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.data = dict()
        self.mouseReleaseEvent = self.beatClicked
        self.highlighted = False

    def setBeatInfo(self, beatInfo):
        self.data['beatInfo'] = beatInfo
        self.data['myIndex'] = len(beatInfo['beats'])

    def beatClicked(self, event):
        print(event.x(), event.y())
        if 'beatInfo' not in self.data:
            pass

        b = self.data['beatInfo']['beats']
        i = self.data['beatInfo']['hIndex']

        if i == self.data['myIndex']:
            # disable this beat
            self.disableHighlight()
            self.data['hIndex'] = -1
        else:
            # disable other highlighted beat
            if i >= 0:
                b[i].disableHighlight()
            # highlight this and mark
            self.setPixmap(QPixmap(':/res/res/track/beat(48x50)_highlighted.png'))
            self.data['beatInfo']['hIndex'] = self.data['myIndex']
            self.highlighted = True

    def disableHighlight(self):
        self.setPixmap(QPixmap(':/res/res/track/beat(48x50).png'))
        self.highlighted = False



if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MainWindow()
    myWindow.show()
    app.exec_()