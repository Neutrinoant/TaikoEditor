import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import Score
from CustomLabel import NoteLabel, BeatLabel
from Command import CommandCreate
from Resource import noteImageList

form_class = uic.loadUiType("mainWindow.ui")[0]

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
        self.highlightBeatLabel=None
        self.score=Score.TJA()
        # print(self.label_beat.width())

# sample code
        self.push_create.clicked.connect(self.push_create_clicked)
        self.undoStack = QUndoStack(self)
        self.donList = []
        self.donNum = 0
#############

    def keyPressEvent(self, e):
        if e.modifiers() & Qt.ControlModifier:
            if e.key() == Qt.Key_Z:
                self.undoStack.undo()
            elif e.key() == Qt.Key_Y:
                self.undoStack.redo()

    # def push_changeOrder_clicked(self):
    #     self.label_don3.raise_()
    #     self.label_don3.stackUnder(self.label_don2)

    def makeLabelNote(self,Note,rendaLen=None):
        noteImage = None
        noteParam = Note.getNote()
        if noteParam in range(0,9): # 9 to be made
            beatSize=[self.label_beat.height(), self.label_beat.height()]
            noteImage= QPixmap(noteImageList[ noteParam ])
            if noteParam in [1,2,5,7]:
                noteImage = noteImage.scaled(beatSize[0]//3, beatSize[1]//3, transformMode=Qt.SmoothTransformation)
            elif noteParam in [3,4,6]:
                noteImage = noteImage.scaled(beatSize[0]//2, beatSize[1]//2, transformMode=Qt.SmoothTransformation)
            # elif note==7:
            #     noteImage = noteImage.scaled(1, beatSize[1]//3, transformMode=Qt.SmoothTransformation,\
            #                                 aspectRatioMode=Qt.KeepAspectRatioByExpanding)
            label = NoteLabel(self.scrollAreaWidgetContents)
            label.setNote(Note)
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
        self.highlightBeatLabel = None
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
                        rendaNote = self.makeLabelNote(note)
                        N = rendaNote
                        rendaStart = curBarPos+beatIdx*w+noteIdx*offset-N.height()/2
                    elif note.getNote()==8:
                        rendaEnd=curBarPos+beatIdx*w+noteIdx*offset-rendaNote.height()/2
                        rendaNote.setRenda(rendaStart,rendaEnd)
                    else:
                        N = self.makeLabelNote(note)
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
        description = 'create don%d' % self.donNum
        command = CommandCreate(self.makeLabelDon, self, description)
        self.undoStack.push(command)
#############

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MainWindow()
    myWindow.show()
    app.exec_()