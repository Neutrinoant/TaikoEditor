import copy

class Bar:
    def __init__(self,measure):
        self.measure=measure
        self.Beat_list=[Beat()]
    def setNoteList(self,RawNoteList):
        #10110101 같은게 들어온다. 8칸이고 메져가 4/4 면 2칸씩 나눈다. 
        l=len(RawNoteList)/self.measure[0]
        cnt=0
        B=Beat(l)
        for note in RawNoteList:
            B.pushNote(note)
            cnt=cnt+1
            if cnt>=l:
                self.Beat_list.append(B)
                cnt=0
                B=Beat(l)



class Beat:
    def __init__(self,split=4):
        self.Note_List=list()
        self.splitParam=int(split) # 한 박자를 몇개로 쪼갤것인가
    def pushNote(self,note):
        if len(self.Note_List)>self.splitParam:
            print("오류:노트넘침")
        N=Note()
        N.setNote(note)
        self.Note_List.append(N)


class Note:
    def __init__(self,BPM=0,noteparam=0,Scroll=1.0,Balloon=None,GOGO=False):
        self.NoteParam=noteparam #0=쉼표 1=동 2=캇 3:큰동 4:큰캇 5:단무지
        self.BPM=BPM
        self.Scroll=Scroll
        self.GOGO=GOGO #True는 고고중 False는 아님
        self.Balloon=Balloon # 풍선 갯수
    def setNote(self,Note):
        self.NoteParam=copy.deepcopy(Note.NoteParam)
        self.BPM=copy.deepcopy(Note.BPM)
        self.Scroll=copy.deepcopy(Note.Scroll)
        self.GOGOStart=copy.deepcopy(Note.GOGO)
        self.Balloon=copy.deepcopy(Note.Balloon)
    def __repr__(self):
        return self.NoteParam








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


