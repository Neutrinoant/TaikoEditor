import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import bisect
import random
import copy
import Score
from CustomLabel import NoteLabel,BeatLabel

form_class = uic.loadUiType("mainWindow.ui")[0]
highlightBeatLabel = None

class MainWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        # self.donIndex_list = []
        # self.don_list = []

        # self.push_changeOrder.clicked.connect(self.push_changeOrder_clicked)
        # self.push_add.clicked.connect(self.push_add_clicked)
        # self.push_del.clicked.connect(self.push_del_clicked)
        # self.push_addBeat.clicked.connect(self.push_addBeat_clicked)
        # self.push_delBeat.clicked.connect(self.push_delBeat_clicked)
        # self.MAX_WIDTH = self.label_beat.width()
        # self.beatInfo = {'beats':[], 'hIndex':-1}

        self.label_beat.setFixedSize(self.scrollArea.height()*2/3,self.scrollArea.height()*2/3)
        self.horizontalLayout.addStretch(1)

        self.push_load.clicked.connect(self.push_load_clicked)
        self.noteList=list()
        self.beatList=list()
        self.score=Score.TJA()
        # print(self.label_beat.width())


    # def push_changeOrder_clicked(self):
    #     self.label_don3.raise_()
    #     self.label_don3.stackUnder(self.label_don2)

    def makeLabelNote(self,note):
        # make label_don
        label = NoteLabel(self.scrollAreaWidgetContents)
        noteImage = None
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
        elif note==7:
            noteImage = QPixmap(':/res/res/note/img_balloon.png')
        elif note==8:
            pass
        else:
            noteImage= QPixmap(':/res/res/note/img_don.png') # will be implemented
            pass  # need other notes (number 5,6,7,8,9)

        beatSize=[self.label_beat.height(),self.label_beat.height()]
        if note>0 and note!=8:
            if note==1 or note==2:
                noteImage = noteImage.scaled(beatSize[0]//3, beatSize[1]//3, transformMode=Qt.SmoothTransformation)
            elif note==3 or note==4:
                noteImage = noteImage.scaled(beatSize[0]//2, beatSize[1]//2, transformMode=Qt.SmoothTransformation)
            elif note==7:
                noteImage = noteImage.scaled(1, beatSize[1]//3, transformMode=Qt.SmoothTransformation,\
                                            aspectRatioMode=Qt.KeepAspectRatioByExpanding)
            label.setPixmap(noteImage)
            label.setFixedSize(noteImage.width(), noteImage.height())

        label.setScaledContents(True)
        label.show()
        return label

    def push_load_clicked(self):
        noteIdx=0
        beatIdx=0
        barIdx=0
        fname = QFileDialog.getOpenFileName(self)[0]
        if fname == '':
            return
        self.score.clearLabel()
        score = Score.TJA(fname)
        track = score.track_list[0]
        for bar in track.bar_list:
            m=bar.measure[0]
            beatIdx=0
            for i in range(len(bar.beat_list)):
                beat=bar.beat_list[i]
                if i==len(bar.beat_list)-1:
                    beat.label=self.makeLabelBeat(end=True)
                else:
                    beat.label=self.makeLabelBeat()
                w,h=beat.label.width(),beat.label.height()
                offset=w//beat.splitParam
                noteIdx=0
                for note in beat.note_list:
                    N=self.makeLabelNote(note.getNote())
                    N.move(w+(barIdx*m+beatIdx)*w+offset*noteIdx-N.height()/2, self.label_beat.y()+self.label_beat.height()/2-N.height()/2)
                    note.label=N
                    noteIdx+=1
                beatIdx+=1
            barIdx+=1
        self.score=score
        # for note in self.noteList:
        #     note.deleteLater()
        # for beat in self.beatList:
        #     beat.deleteLater()

        # self.noteList=list()
        # self.beatList=list()
        # self.measureList=list()
        
        # rendaInfo = {'flag':False, 'note':0, 'barIdx':0, 'splitIdx':0}
        # barIdx = 0

        # for bar in track.bar_list:
        #     m = bar.measure
        #     tempBeatList = [self.makeLabelBeat() for _ in range(m[0]-1)]
        #     tempBeatList.append(self.makeLabelBeat(end=True))
        #     beatIdx = 0

        #     for beat in bar.beat_list:
        #         w, h = tempBeatList[beatIdx].width(), tempBeatList[beatIdx].height()
        #         splitNum = beat.splitParam
        #         offset = tempBeatList[0].width() // splitNum
        #         tempNoteList=list()

        #         for note in beat.note_list:
        #             N=self.makeLabelNote(note.getNote())
        #             N.setNote(note)
        #             tempNoteList.append(N)

        #         for i in range(len(tempNoteList)):
        #             tempNoteList[i].move(w+(barIdx*m[0]+beatIdx)*w+offset*i-tempNoteList[i].height()/2, self.label_beat.y()+self.label_beat.height()/2-tempNoteList[i].height()/2)  # need modify
                
        #         beatIdx += 1
        #         self.noteList += tempNoteList

        #     barIdx += 1
        #     self.beatList.append(tempBeatList)
        #     self.measureList.append(m)

        # self.score = score
        

            

    def makeLabelBeat(self, end=False):
        # make new img_beat
        if not end:
            beatImage = QPixmap(':/res/res/track/beat(48x50).png')
        else:
            beatImage = QPixmap(':/res/res/track/beat_end(48x50).png')
        label = BeatLabel(self.scrollAreaWidgetContents)                   # 후에 BeatLabe class 만들어야함.
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



if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MainWindow()
    myWindow.show()
    app.exec_()