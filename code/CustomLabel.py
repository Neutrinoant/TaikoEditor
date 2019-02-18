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
    def setNote(self,Note):
        self.note=Note
    #start: left-top of first note, End: left-top of last note
    def setRenda(self,rendaStart,rendaEnd):
        noteWidth = self.width()
        noteHeight = self.height()
        midWidth = rendaEnd-rendaStart
        self.setFixedSize(midWidth+noteWidth, noteWidth)
        if self.note.getNote() != 7:
            if self.note.getNote()==5:
                head = QPixmap(':/res/res/note/img_renda_head.png')
                mid = QPixmap(':/res/res/note/img_renda_middle.png')
                tail = QPixmap(':/res/res/note/img_renda_tail.png')
            elif self.note.getNote()==6:
                head = QPixmap(':/res/res/note/img_renda_big_head.png')
                mid = QPixmap(':/res/res/note/img_renda_big_middle.png')
                tail = QPixmap(':/res/res/note/img_renda_big_tail.png')
            rendaPixmap = QPixmap(rendaEnd-rendaStart+noteWidth,noteHeight)
            rendaPixmap.fill(Qt.transparent)
            rendaPainter = QPainter(rendaPixmap)
            rendaPainter.setRenderHint(QPainter.SmoothPixmapTransform)
            rendaPainter.drawPixmap(QRect(midWidth,0,noteWidth,noteHeight),tail)
            rendaPainter.drawPixmap(QRect(noteWidth//2,0,midWidth,noteHeight),mid)
            rendaPainter.drawPixmap(QRect(0,0,noteWidth,noteHeight),head)
            rendaPainter.end()
            self.setPixmap(rendaPixmap)
        else: # note = 7
            head = QPixmap(':/res/res/note/img_balloon_head.png')
            tail = QPixmap(':/res/res/note/img_balloon_tail.png')


        
    
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

