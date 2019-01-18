
class Note:
    def __init__(self,noteparam=0):
        self.NoteParam=0 #0=쉼표 1=동 2=캇 3:큰동 4:큰캇 5:단무지
        self.BPMChange=0
        self.ScrollChange=0
        self.GOGOStart=1 #1은 시작, 2는 끝
        self.Balloon=0 # 풍선 갯수

class Bar:
    def __init__(self,measure):
        self.measure=measure
        self.Beat_list=[Beats()]*measure[1]

class Beats:
    def __init__(self,split=4):
        self.splitParam=split # 한 박자를 몇개로 쪼갤것인가
        self.Notelist=[Note(0)]*split
        self.curNoteIdx=0
    def pushNote(self,noteParam):
        self.curNoteIdx=self.curNoteIdx+1
        if curNoteIdx>=self.splitParam:
            print("노트 넘침")
        Notelist[curNoteIdx]=Note(noteparam)





class Track:
    def __init__(self):
        self.bar_list=list()
        self.COURSE=0 #0:간단 1: 보통 2: 무즙 3: 오니 4: 우라
        self.LEVEL=0
        self.SCOREINIT=0
        self.SCOREDIFF=0
        self.STYLE=1
    def pushBar(self,bar):
        self.bar_list.append(bar)
    def print(self):
        print(self)
    def __repr__(self):
        return str([self.COURSE,self.LEVEL,self.SCOREINIT,self.SCOREDIFF,self.STYLE])

class TJA:
    def __init__(self):
        self.Track_list=list()
        self.TITLE="default"
        self.SUBTITLE="default"
        self.BPM=100
        self.WAVE=""
        self.SONGVOL=100.0
        self.SEVOL=100.0
        self.OFFSET=0
        self.DEMOSTART=0.0
        self.SIDE=3
        self.SCOREMODE=2
        self.GENRE="default"
        self.GAME=''
        self.LIFE=''
    def newTrack(self):
        self.Track_list.append(Track())
    def print(self):
        print(self)
        for Tr in self.Track_list:
            Tr.print()
    def __repr__(self):
        return str([self.TITLE,self.SUBTITLE,self.BPM,self.WAVE,self.SONGVOL,self.SEVOL,self.OFFSET,self.DEMOSTART,self.SIDE,self.SCOREMODE,self.GENRE,self.GAME,self.LIFE])

