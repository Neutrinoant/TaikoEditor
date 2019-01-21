import copy

class Bar:
    def __init__(self,measure):
        self.measure=copy.deepcopy(measure)
        self.Beat_list=[Beat() for _ in range(measure[0])]
    def setNoteList(self,RawNoteList):
        #10110101 같은게 들어온다. 8칸이고 메져가 4/4 면 2칸씩 나눈다.
        # print(RawNoteList) 
        l=len(RawNoteList)/self.measure[0]
        # print(l)
        if l<1:
            l=1
            #1->1000으로 바꿔주는 과정이 필요. 우선 전체 길이를 1/l 배 만큼 늘려야한다.
            #기본적으로 한개 들어간다고 생각하고, 0인 노트를 1/l-1 개 만큼 복사해서 넣어준다고 생각하자. 
            NewRawNoteList=list()
            for n in RawNoteList:
                NewRawNoteList.append(n)
                for _ in range(int(1/l)-1):
                    N=Note()
                    N.setNote(n)
                    N.setZero()
                    NewRawNoteList.append(N)
            RawNoteList=NewRawNoteList
        idxoffset=1
        cnt=0
        BeatListIdx=0
        for B in self.Beat_list:
            B.setSplit(l)
        for note in RawNoteList:
            # print(BeatListIdx)
            self.Beat_list[BeatListIdx].pushNote(note)
            cnt=cnt+1
            if cnt>=l:
                BeatListIdx=BeatListIdx+idxoffset
                cnt=0
    def __repr__(self):
        s=str()
        for b in self.Beat_list:
            s=s+str(b)+" "
        return s



class Beat:
    def __init__(self,split=4):
        self.Note_List=list()
        self.splitParam=int(split) # 한 박자를 몇개로 쪼갤것인가
    def setSplit(self,split):
        self.splitParam=split
    def pushNote(self,note):
        if len(self.Note_List)==self.splitParam:
            print("오류:노트넘침")
            print(self.splitParam)
            quit()
        N=Note()
        N.setNote(note)
        self.Note_List.append(N)
    def __repr__(self):
        s=str()
        for note in self.Note_List:
            s=s+str(note)
        return s


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
    def setZero(self):
        self.NoteParam=0
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
        for bar in self.bar_list:
            print(bar)
    def toTJAForm(self):
        s=str()
        






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
    def toTJAForm(self):
        s=str()
        s=s+"TITLE:"+str(self.TITLE)+"\n"
        s=s+"SUBTITLE:"+str(self.SUBTITLE)+"\n"
        s=s+"BPM:"+str(self.BPM)+"\n"
        s=s+"WAVE:"+str(self.WAVE)+"\n"
        s=s+"SONGVOL:"+str(self.SONGVOL)+"\n"
        s=s+"SEVOL:"+str(self.SEVOL)+"\n"
        s=s+"OFFSET:"+str(self.OFFSET)+"\n"
        s=s+"DEMOSTART:"+str(self.DEMOSTART)+"\n"
        s=s+"SIDE:"+str(self.SIDE)+"\n"
        s=s+"SCOREMODE:"+str(self.SCOREMODE)+"\n"
        s=s+"GENRE:"+str(self.GENRE)+"\n"
        s=s+"\n"
        for track in self.Track_list:
            s=s+"COURSE:"+str(track.COURSE)+"\n"
            s=s+"LEVEL:"+str(track.LEVEL)+"\n"

            if track.SCOREINIT==0:
                s=s+"SCOREINIT:"+"\n"
            else:
                s=s+"SCOREINIT:"+str(track.SCOREINIT)+"\n"
            if track.SCOREDIFF==0:
                s=s+"SCOREDIFF:"+"\n"
            else:
                s=s+"SCOREDIFF:"+str(track.SCOREDIFF)+"\n"

            s=s+"STYLE:"+str(track.STYLE)+"\n"

            
            curMeasure=[4,4]
            curBPM=self.BPM
            BallonList=list()
            for bar in track.bar_list:
                for beat in bar.Beat_list:
                    for note in beat.Note_List:
                        if note.NoteParam=='7':
                            BallonList.append(note.Balloon)
            s=s+"BALLOON:"
            for i in BallonList:
                s=s+i+","
                
            s=s+"\n"+"#START"+"\n"
            s=s+"#END"+"\n"
        
        return s


    def __repr__(self):
        return str([self.TITLE,self.SUBTITLE,self.BPM,self.WAVE,self.SONGVOL,self.SEVOL,self.OFFSET,self.DEMOSTART,self.SIDE,self.SCOREMODE,self.GENRE,self.GAME,self.LIFE])


