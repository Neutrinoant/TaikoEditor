import copy

class Bar:
    def __init__(self,measure):
        self.measure=copy.deepcopy(measure)
        self.beat_list=[Beat() for _ in range(measure[0])]
    def setNoteList(self,rawNoteList):
        #10110101 같은게 들어온다. 8칸이고 메져가 4/4 면 2칸씩 나눈다.
        # print(rawNoteList) 
        l=len(rawNoteList)/self.measure[0]
        # print(l)
        if l<1:
            l=1
            #1->1000으로 바꿔주는 과정이 필요. 우선 전체 길이를 1/l 배 만큼 늘려야한다.
            #기본적으로 한개 들어간다고 생각하고, 0인 노트를 1/l-1 개 만큼 복사해서 넣어준다고 생각하자. 
            newRawNoteList=list()
            for n in rawNoteList:
                newRawNoteList.append(n)
                for _ in range(int(1/l)-1):
                    N=Note()
                    N.setNote(n)
                    N.setZero()
                    newRawNoteList.append(N)
            rawNoteList=newRawNoteList
        idxOffset=1
        cnt=0
        beatListIdx=0
        for B in self.beat_list:
            B.setSplit(l)
        for note in rawNoteList:
            # print(beatListIdx)
            self.beat_list[beatListIdx].pushNote(note)
            cnt=cnt+1
            if cnt>=l:
                beatListIdx=beatListIdx+idxOffset
                cnt=0
    def __repr__(self):
        s=str()
        for b in self.beat_list:
            s=s+str(b)+" "
        return s



class Beat:
    def __init__(self,split=4):
        self.note_list=list()
        self.splitParam=int(split) # 한 박자를 몇개로 쪼갤것인가
    def setSplit(self,split):
        self.splitParam=split
    def pushNote(self,note):
        if len(self.note_list)==self.splitParam:
            print("오류:노트넘침")
            print(self.splitParam)
            quit()
        N=Note()
        N.setNote(note)
        self.note_list.append(N)
    def __repr__(self):
        s=str()
        for note in self.note_list:
            s=s+str(note)
        return s


class Note:
    def __init__(self,BPM=0,noteParam=0,scroll=1.0,balloon=None,GOGO=False):
        self.noteParam=noteParam #0=쉼표 1=동 2=캇 3:큰동 4:큰캇 5:단무지
        self.BPM=BPM
        self.scroll=scroll
        self.GOGO=GOGO #True는 고고중 False는 아님
        self.balloon=balloon # 풍선 갯수
    def setNote(self,Note):
        self.noteParam=copy.deepcopy(Note.noteParam)
        self.BPM=copy.deepcopy(Note.BPM)
        self.scroll=copy.deepcopy(Note.scroll)
        self.GOGOStart=copy.deepcopy(Note.GOGO)
        self.balloon=copy.deepcopy(Note.balloon)
    def setZero(self):
        self.noteParam=0
    def __repr__(self):
        return self.noteParam


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
        self.track_list=list()
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
        self.track_list.append(Track())
    def print(self):
        print(self)
        for Tr in self.track_list:
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
        for track in self.track_list:
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
            ballonList=list()
            for bar in track.bar_list:
                for beat in bar.beat_list:
                    for note in beat.note_list:
                        if note.noteParam=='7':
                            ballonList.append(note.balloon)
            s=s+"BALLOON:"
            for i in ballonList:
                s=s+i+","
                
            s=s+"\n"+"#START"+"\n"
            s=s+"#END"+"\n"
        
        return s

    def __repr__(self):
        return str([self.TITLE,self.SUBTITLE,self.BPM,self.WAVE,self.SONGVOL,self.SEVOL,self.OFFSET,self.DEMOSTART,self.SIDE,self.SCOREMODE,self.GENRE,self.GAME,self.LIFE])
