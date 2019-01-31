from PyQt5.QtWidgets import QLabel 
from PyQt5.QtGui import *
import Score
highlightBeatLabel = None

class NoteLabel(QLabel):
    def __init__(self,parent):
        super().__init__(parent)
        self.note=Score.Note()
    def setNote(self,Note):
        self.note.setNote(Note)
    
class BeatLabel(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.mousePressEvent = self.beatClicked
        self.highlighted = False

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

