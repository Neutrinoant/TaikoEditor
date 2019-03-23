from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic
import Score
from Command import CommandChangeNote

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
        description = 'change note %d to %d'%(self.note.noteParam,noteIdx)
        command = CommandChangeNote(self, noteIdx, description)
        self.window().undoStack.push(command)

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
        if self.window().highlightBeatLabel != None:
            # disable other highlighted beat
            self.window().highlightBeatLabel.disableHighlight()

        # highlight this label
        self.setPixmap(QPixmap(':/res/res/track/beat(48x50)_highlighted.png'))
        self.highlighted = True
        self.window().highlightBeatLabel = self

    def disableHighlight(self):
        self.setPixmap(QPixmap(':/res/res/track/beat(48x50).png'))
        self.highlighted = False

class CommandChangeNote(QUndoCommand):

    def __init__(self, label, noteIdx, description):
        super(CommandChangeNote, self).__init__(description)
        self.label = label  # function
        self.newIdx = noteIdx
        self.oldIdx = label.note.noteParam

    def redo(self):
        self._changeNote(self.newIdx)

    def undo(self):
        self._changeNote(self.oldIdx)
    
    def _changeNote(self, noteIdx):
        from Resource import noteImageList
        newImage=QPixmap(noteImageList[ noteIdx ]) #1-2-3-4 가 돌아간다
        if noteIdx in range(1,5):
            beatHeight = self.label.parentWidget().layout().itemAt(0).widget().height()
            beatSize=[beatHeight, beatHeight]
            if noteIdx in [1,2]:
                newImage = newImage.scaled(beatSize[0]//3, beatSize[1]//3, transformMode=Qt.SmoothTransformation)
            elif noteIdx in [3,4]:
                newImage = newImage.scaled(beatSize[0]//2, beatSize[1]//2, transformMode=Qt.SmoothTransformation)
            self.label.move(self.label.x()+self.label.width()//2, self.label.y()+self.label.height()//2)
            self.label.note.noteParam=noteIdx
            self.label.setPixmap(newImage)
            self.label.setFixedSize(newImage.width(), newImage.height())
            self.label.move(self.label.x()-self.label.width()//2, self.label.y()-self.label.height()//2)
            self.label.show()