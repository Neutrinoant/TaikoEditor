from PyQt5.QtWidgets import QLabel 
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic
import Score

highlightBeatLabel = None

class NoteLabel(QLabel):
    def __init__(self,parent):
        super().__init__(parent)
        self.note=Score.Note()
        self.mousePressEvent = self.NoteClicked
    def setNote(self,Note):
        self.note=Note

    def NoteClicked(self,event):
        if self.note.noteParam in [0,8]:
            return
        self.changeNote((self.note.noteParam)%4+1)

    def changeNote(self,noteIdx):
        from TJAEditor import noteImageList
        newImage=QPixmap(noteImageList[ noteIdx ]) #1-2-3-4 가 돌아간다
        if noteIdx>0 and noteIdx!=8:
            beatHeight = self.parentWidget().layout().itemAt(0).widget().height()
            beatSize=[beatHeight, beatHeight]
            if noteIdx in [1,2]:
                newImage = newImage.scaled(beatSize[0]//3, beatSize[1]//3, transformMode=Qt.SmoothTransformation)
            elif noteIdx in [3,4]:
                newImage = newImage.scaled(beatSize[0]//2, beatSize[1]//2, transformMode=Qt.SmoothTransformation)
            # elif note==7:
            #     newImage = newImage.scaled(1, beatSize[1]//3, transformMode=Qt.SmoothTransformation,\
            #                                 aspectRatioMode=Qt.KeepAspectRatioByExpanding)
            self.move(self.x()+self.width()//2, self.y()+self.height()//2)
            self.note.noteParam=noteIdx
            self.setPixmap(newImage)
            self.setFixedSize(newImage.width(), newImage.height())
            self.move(self.x()-self.width()//2, self.y()-self.height()//2)
            self.show()

    #start: left-top of first note, End: left-top of last note
    def setRenda(self,rendaStart,rendaEnd):
        noteNum = self.note.getNote()
        noteWidth = self.width()
        noteHeight = self.height()
        midWidth = rendaEnd-rendaStart
        self.setFixedSize(midWidth+noteWidth, noteHeight)

        if self.note.getNote()==5:
            head = QPixmap(':/res/res/note/img_renda_head.png')
            mid = QPixmap(':/res/res/note/img_renda_middle.png')
            tail = QPixmap(':/res/res/note/img_renda_tail.png')
        elif self.note.getNote()==6:
            head = QPixmap(':/res/res/note/img_renda_big_head.png')
            mid = QPixmap(':/res/res/note/img_renda_big_middle.png')
            tail = QPixmap(':/res/res/note/img_renda_big_tail.png')
        elif self.note.getNote()==7:
            head = QPixmap(':/res/res/note/img_balloon_head.png')
            mid = QPixmap(':/res/res/note/img_balloon_middle.png')
            tail = QPixmap(':/res/res/note/img_balloon_tail.png')

        rendaPixmap = QPixmap(rendaEnd-rendaStart+noteWidth,noteHeight)
        rendaPixmap.fill(Qt.transparent)
        rendaPainter = QPainter(rendaPixmap)
        rendaPainter.setRenderHint(QPainter.SmoothPixmapTransform)
        rendaPainter.drawPixmap(QRect(midWidth,0,noteWidth,noteHeight),tail)
        rendaPainter.drawPixmap(QRect(noteWidth//2,0,midWidth,noteHeight),mid)
        rendaPainter.drawPixmap(QRect(0,0,noteWidth,noteHeight),head)
        rendaPainter.end()
        self.setPixmap(rendaPixmap)
            


        
    
class BeatLabel(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.mousePressEvent = self.beatClicked
        self.highlighted = False
        self.beat=Score.Beat()
    
    def setBeat(self,Beat):
        self.beat=Beat

    def beatClicked(self, event):
        global highlightBeatLabel
        if highlightBeatLabel != None:
            # disable other highlighted beat
            highlightBeatLabel.disableHighlight()

        # highlight this label
        self.setPixmap(QPixmap(':/res/res/track/beat(48x50)_highlighted.png'))
        self.highlighted = True
        highlightBeatLabel = self

    def disableHighlight(self):
        self.setPixmap(QPixmap(':/res/res/track/beat(48x50).png'))
        self.highlighted = False

