import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import bisect
import random
import copy
import Score
import math
from CustomLabel import NoteLabel,BeatLabel
import math

form_class = uic.loadUiType("mainWindow.ui")[0]
highlightBeatLabel = None
donList = []
donNum = 0

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
        self.push_save.clicked.connect(self.push_save_clicked)
        self.noteList=list()
        self.beatList=list()
        self.score=Score.TJA()
        # print(self.label_beat.width())

# sample code
        self.undoStack = QUndoStack(self)
        self.push_create.clicked.connect(self.push_create_clicked)
        self.push_redo.clicked.connect(self.undoStack.redo)
        self.push_undo.clicked.connect(self.undoStack.undo)
#############


    # def push_changeOrder_clicked(self):
    #     self.label_don3.raise_()
    #     self.label_don3.stackUnder(self.label_don2)

    def makeLabelNote(self,note,rendaLen=None):
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
        elif note==5:
            noteImage= QPixmap(':/res/res/note/img_renda_head.png')
        elif note==6:
            noteImage= QPixmap(':/res/res/note/img_renda_big_head.png')
        elif note==7:
            noteImage= QPixmap(':/res/res/note/img_balloon_head.png')
        elif note==8:
            pass
        else:
            noteImage= QPixmap(':/res/res/note/img_don.png') # will be implemented
            pass  # need other notes (number 9)

        beatSize=[self.label_beat.height(),self.label_beat.height()]
        if note>0 and note!=8:
            if note in [1,2,5,7]:
                noteImage = noteImage.scaled(beatSize[0]//3, beatSize[1]//3, transformMode=Qt.SmoothTransformation)
            elif note in [3,4,6]:
                noteImage = noteImage.scaled(beatSize[0]//2, beatSize[1]//2, transformMode=Qt.SmoothTransformation)
            # elif note==7:
            #     noteImage = noteImage.scaled(1, beatSize[1]//3, transformMode=Qt.SmoothTransformation,\
            #                                 aspectRatioMode=Qt.KeepAspectRatioByExpanding)

            label.setPixmap(noteImage)
            label.setFixedSize(noteImage.width(), noteImage.height())

        label.setScaledContents(True)
        label.show()
        return label
    
    def push_save_clicked(self):
        fname=QFileDialog.getSaveFileName(self)[0]
        print(fname)
        file=open(fname,'w')
        file.write(self.score.toTJAForm())
        file.close()

    def push_load_clicked(self):
        rendaflag=False
        rendaNote,rendaStart,rendaEnd = None,None,None
        fname = QFileDialog.getOpenFileName(self)[0]
        if fname == '':
            return
        # fname="test.tja"
        self.score.clearLabel()
        score = Score.TJA(fname)
        track = score.track_list[0]
        curBarPos = self.label_beat.width() # left-most absolute position x of current bar
        barIdx = 0
        for bar in track.bar_list:
            m = bar.measure[0]
            beatIdx = 0
            for beat in bar.beat_list:
                if beatIdx == len(bar.beat_list)-1:
                    beat.label = self.makeLabelBeat(end=True)
                else:
                    beat.label = self.makeLabelBeat()
                w = beat.label.width()
                offset = w/beat.splitParam # distance between notes
                noteIdx = 0
                for note in beat.note_list:
                    if note.getNote() in [5,6,7]:
                        rendaNote = self.makeLabelNote(note.getNote())
                        N = rendaNote
                        rendaStart = curBarPos+beatIdx*w+noteIdx*offset-N.height()/2
                    elif note.getNote()==8:
                        rendaEnd=curBarPos+beatIdx*w+noteIdx*offset-rendaNote.height()/2
                        rendaNote.setRenda(rendaStart,rendaEnd)
                    else:
                        N = self.makeLabelNote(note.getNote())
                    N.setNote(note)
                    N.move(round(curBarPos+beatIdx*w+noteIdx*offset-N.height()/2), round(self.label_beat.y()+self.label_beat.height()/2-N.height()/2))
                    note.label = N
                    noteIdx+=1
                    # print(N.x())
                beatIdx+=1
            curBarPos += m*w
            barIdx+=1
        self.score=score
        # self.score.print()
        print(self.score.toTJAForm())

            

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



# sample code
    def makeLabelDon(self):
        # make label_don
        label = NoteLabel(self.scrollAreaWidgetContents_2)
        noteImage= QPixmap(':/res/res/note/img_don.png')
        beatSize=[self.label_beat.height(),self.label_beat.height()]
        noteImage = noteImage.scaled(50, 50, transformMode=Qt.SmoothTransformation)
        label.setPixmap(noteImage)
        label.setFixedSize(noteImage.width(), noteImage.height())
        label.setScaledContents(True)
        label.show()
        return label
    def push_create_clicked(self):
        global donNum
        description = 'create don%d' % donNum
        command = CommandCreate(self.makeLabelDon, description)
        self.undoStack.push(command)
#############

# sample code
class CommandCreate(QUndoCommand):

    def __init__(self, makeDon, description):
        super(CommandCreate, self).__init__(description)
        self.makeDon = makeDon  # function

    def redo(self):
        don = self.makeDon()
        global donNum
        global donList
        don.setObjectName('don%d' % donNum)
        don.move(donNum*don.width()//10, 0)
        donList.append(don)
        donNum += 1

    def undo(self):
        global donNum
        global donList
        don = donList.pop()
        don.deleteLater()
        donNum -= 1
#############

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MainWindow()
    myWindow.show()
    app.exec_()