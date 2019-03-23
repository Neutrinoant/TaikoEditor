from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from Resource import noteImageList

class CommandCreate(QUndoCommand):

    def __init__(self, makeDon, parent, description):
        super(CommandCreate, self).__init__(description)
        self.makeDon = makeDon  # function
        self.window = parent.window()

    def redo(self):
        don = self.makeDon()
        don.setObjectName('don%d' % self.window.donNum)
        don.move(self.window.donNum*don.width()//10, 0)
        self.window.donList.append(don)
        self.window.donNum += 1

    def undo(self):
        don = self.window.donList.pop()
        don.deleteLater()
        self.window.donNum -= 1
        

        
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