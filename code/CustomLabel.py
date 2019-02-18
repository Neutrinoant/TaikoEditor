from PyQt5.QtWidgets import QLabel 
from PyQt5.QtGui import *
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
        if self.note.getNote()==5:
            head = QPixmap(':/res/res/note/img_renda_head.png')
            mid = QPixmap(':/res/res/note/img_renda_middle.png')
            tail = QPixmap(':/res/res/note/img_renda_tail.png')
        else:  # note == 6
            head = QPixmap(':/res/res/note/img_renda_big_head.png')
            mid = QPixmap(':/res/res/note/img_renda_big_middle.png')
            tail = QPixmap(':/res/res/note/img_renda_big_tail.png')
        rendaPainter = QPainter()
        
    
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

