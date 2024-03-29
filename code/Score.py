import copy
import re
import codecs
import sys
import math

def LCM(a,b):
    return a*b//math.gcd(a,b)

class Bar:
    def __init__(self,measure):
        self.measure=copy.deepcopy(measure)
        self.beat_list=[Beat(parent=self) for _ in range(measure[0])]
    def changeMeasaure(self,measure,idx):
        #분자를 바꿀거면 1 분모를 바꿀거면 2
        self.measure[idx-1]=copy.deepcopy(measure)
        self.beat_list=self.beat_list[0:measure[0]]
    def setNoteList(self,rawNoteList):
        #10110101 같은게 들어온다. 8칸이고 메져가 4/4 면 2칸씩 나눈다.
        if len(rawNoteList)%self.measure[0]!=0:
            #case 1 : 작을때, case 2: 클 때 
            # 메져가 4고 길이가 6개. 전체길이는 12개가 되어야한다.
            # 메져가 4고 길이가 2개, 전체길이는 4개가 되어야한다. 
            # 새 길이는 둘의 최소공배수가 되어야한다.
            newLen=LCM(len(rawNoteList),self.measure[0])
            exParam=int(newLen/len(rawNoteList)) # 여기서 만들어진 exParam이 노트 1개를 몇배로 늘릴것인지의 척도가 된다. 
            # print(exParam)
            newRawNoteList=list()
            for n in rawNoteList:
                newRawNoteList.append(n)
                for _ in range(exParam-1):
                    N=Note()
                    N.setNote(n)
                    N.setZero()
                    newRawNoteList.append(N)
            rawNoteList=newRawNoteList
        l=len(rawNoteList)/self.measure[0]
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
    def clearLabel(self):
        for beat in self.beat_list:
            beat.clearLabel()
    def __repr__(self):
        s=str()
        s+=str(self.measure[0])+" "+str(self.measure[1])+"\n"
        for b in self.beat_list:
            s=s+str(b)+" "
        return s



class Beat:
    def __init__(self,parent=None,split=4):
        self.note_list=list()
        self.splitParam=int(split) # 한 박자를 몇개로 쪼갤것인가
        self.parentBar=parent
        self.label=None
    def clearLabel(self):
        for note in self.note_list:
            note.deleteLabel()
        self.deleteLabel()
    def deleteLabel(self):
        if self.label==None:
            return
        self.label.deleteLater()
        self.label=None
    def setSplit(self,split):
        self.splitParam=split
    def pushNote(self,note):
        if len(self.note_list)==self.splitParam:
            print("오류:노트넘침")
            print(self.splitParam)
            quit()
        note.setParent(self)
        self.note_list.append(note)
    def getParent(self):
        return self.parentBar
    def __repr__(self):
        s=str()
        for note in self.note_list:
            s=s+str(note)
        return s


class Note:
    def __init__(self,parent=None,BPM=0,noteParam='0',scroll=1.0,balloon=None,GOGO=False):
        self.noteParam=int(noteParam) #0=쉼표 1=동 2=캇 3:큰동 4:큰캇 5:단무지
        self.BPM=BPM
        self.scroll=scroll
        self.GOGO=GOGO #True는 고고중 False는 아님
        self.balloon=balloon # 풍선 갯수
        self.parentBeat=parent
        self.label=None
    def setNote(self,Note):
        self.noteParam=copy.deepcopy(Note.noteParam)
        self.BPM=copy.deepcopy(Note.BPM)
        self.scroll=copy.deepcopy(Note.scroll)
        self.GOGOStart=copy.deepcopy(Note.GOGO)
        self.balloon=copy.deepcopy(Note.balloon)
        self.parentBeat=Note.parentBeat
    def setLabel(self,Label):
        self.label=Label
    def deleteLabel(self):
        if self.label==None:
            return
        self.label.deleteLater()
        self.label=None
    def setZero(self):
        self.noteParam=0
    def getNote(self):
        return int(self.noteParam)
    def getParent(self):
        return self.parentBeat
    def setParent(self,parent):
        self.parentBeat=parent
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
    def clearLabel(self):
        for bar in self.bar_list:
            bar.clearLabel()
    # def toTJAForm(self):
    #     s=str()
    def __repr__(self):
        return str([self.COURSE,self.LEVEL,self.SCOREINIT,self.SCOREDIFF,self.STYLE])



class TJA:
    def __init__(self,fname=None):
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
    
        if fname==None:
            return
        
        with codecs.open(fname, "r", encoding='shift-jis', errors='ignore') as f:
            s=f.read().splitlines()

        rawData=list()
        courseNum=0
        for i in s:
            if i=='':
                continue
            else:
                k=re.sub('//(.*)','',i)
                r=re.match('COURSE:(.*)',k)
                if r!=None:
                    courseNum=courseNum+1

                rawData.append(k)

        if courseNum==0:
            courseNum=1

        self.track_list=[Track() for _ in range(courseNum)]
        curTrIdx=0
        curBalloonList=list()
        flag=False
        l=len(rawData)
        for line in rawData:
            if not flag:
                #곡 전체 데이터
                s=re.match('TITLE:(.*)',line)
                if s!=None:
                    self.TITLE=s.group(1)
                    continue
                s=re.match('SUBTITLE:(.*)',line)
                if s!=None:
                    self.SUBTITLE=s.group(1)
                    continue
                s=re.match('BPM:(.*)',line)
                if s!=None:
                    self.BPM=int(s.group(1))
                    continue
                s=re.match('WAVE:(.*)',line)
                if s!=None:
                    self.WAVE=s.group(1)
                    continue
                s=re.match('SONGVOL:(.*)',line)
                if s!=None:
                    self.SONGVOL=int(s.group(1))
                    continue
                s=re.match('SEVOL:(.*)',line)
                if s!=None:
                    self.SEVOL=int(s.group(1))
                    continue
                s=re.match('OFFSET:(.*)',line)
                if s!=None:
                    self.OFFSET=float(s.group(1))
                    continue
                s=re.match('DEMOSTART:(.*)',line)
                if s!=None:
                    self.DEMOSTART=float(s.group(1))
                    continue
                s=re.match('SIDE:(.*)',line)
                if s!=None:
                    self.SIDE=int(s.group(1))
                    continue
                s=re.match('SCOREMODE:(.*)',line)
                if s!=None:
                    self.SCOREMODE=int(s.group(1))
                    continue
                s=re.match('GENRE:(.*)',line)
                if s!=None:
                    self.GENRE=s.group(1)
                    continue

                #코스별 데이터
                s=re.match('COURSE:(.*)',line)
                if s!=None:
                    self.track_list[curTrIdx].COURSE=s.group(1)
                    # print(s.group(1))
                    continue
                s=re.match('LEVEL:(.*)',line)
                if s!=None:
                    self.track_list[curTrIdx].LEVEL=int(s.group(1))
                    continue
                s=re.match('SCOREINIT:(.*)',line)
                if s!=None:
                    if s.group(1) == '':
                        continue
                    self.track_list[curTrIdx].SCOREINIT=int(s.group(1))
                    continue
                s=re.match('SCOREDIFF:(.*)',line)
                if s!=None:
                    if s.group(1) == '':
                        continue
                    self.track_list[curTrIdx].SCOREDIFF=int(s.group(1))
                    continue
                s=re.match('BALLOON:(.*)',line)
                if s!=None:
                    if s.group(1) == '':
                        continue
                    curBalloonList=s.group(1).split(',')
                    # print(curBalloonList)
                    continue
                s=re.match('STYLE:(.*)',line)
                if s!=None:
                    if s.group(1) == '':
                        continue
                    self.track_list[curTrIdx].STYLE=s.group(1)
                    continue
                if line=='#START':
                    flag=True
                    curGOGO=False
                    curSCROLL=1.0
                    curBPM=self.BPM
                    curMEASURE=[4,4]
                    tempList=list()
                    balloonIdx=0
            #보면 파싱하기
            else:
                if line=='#END':
                    flag=False
                    # self.track_list[curTrIdx].bar_list=makeBarList(bar,self.BPM,curBalloonList)
                    curTrIdx=curTrIdx+1
                else:
                    if line[0]=='#':
                        if line=='#GOGOSTART':
                            curGOGO=True
                        if line=='#GOGOEND':
                            curGOGO=False
                        s=re.match('#SCROLL (.*)',line)
                        if s!=None:
                            curSCROLL=float(s.group(1))
                            continue
                        s=re.match('#BPMCHANGE (.*)',line)
                        if s!=None:
                            curBPM=float(s.group(1))
                            continue
                        s=re.match("#MEASURE (.*)/(.*)",line)
                        if s!=None:
                            curMEASURE[0]=int(s.group(1))
                            curMEASURE[1]=int(s.group(2))
                            
                            continue
                    else:
                        for note in line:
                            if note==',':
                                if len(tempList)==0:
                                    tempList.append(Note(None,curBPM,'0',curSCROLL,None,curGOGO))
                                B=Bar(curMEASURE)
                                print(curMEASURE)
                                B.setNoteList(tempList)
                                self.track_list[curTrIdx].pushBar(B)
                                tempList=list()
                            elif note=='7':
                                tempList.append(Note(None,curBPM,note,curSCROLL,curBalloonList[balloonIdx],curGOGO))
                                balloonIdx=balloonIdx+1
                            else:
                                tempList.append(Note(None,curBPM,note,curSCROLL,None,curGOGO))


    def newTrack(self):
        self.track_list.append(Track())
    def print(self):
        print(self)
        for Tr in self.track_list:
            Tr.print()
    def clearLabel(self):
        for tr in self.track_list:
            tr.clearLabel()

    
    def toTJAForm(self):
        s=str()
        curline=""
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
            s=s+"\n"
            s=s+"COURSE:"+str(track.COURSE)+"\n"
            s=s+"LEVEL:"+str(track.LEVEL)+"\n"
            s=s+"SCOREINIT:"+str(track.SCOREINIT)+"\n"
            s=s+"SCOREDIFF:"+str(track.SCOREDIFF)+"\n"
            s=s+"STYLE:"+str(track.STYLE)+"\n"
            curMeasure=[4,4]
            curBPM=self.BPM
            curGOGO=False
            curSCROLL=1.0
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
            for bar in track.bar_list:
                if curMeasure[0] != bar.measure[0] or curMeasure[1] != bar.measure[1]:
                    curMeasure=copy.deepcopy(bar.measure)
                    s+="#MEASURE "+ str(bar.measure[0])+"/"+str(bar.measure[1])+"\n"
                for beat in bar.beat_list:
                    for note in beat.note_list:
                        if curBPM != note.BPM:
                            curBPM=note.BPM
                            if curline!="":
                                s+=curline+"\n"
                                curline=""
                            s+="#BPMCHANGE "+str(curBPM)+"\n"
                        if not curGOGO and note.GOGO:
                            if curline!="":
                                s+=curline+"\n"
                                curline=""
                            s+="#GOGOSTART\n"
                            curGOGO=True
                        elif curGOGO and not note.GOGO:
                            if curline!="":
                                s+=curline+"\n"
                                curline=""
                            s+="#GOGOEND\n"
                            curGOGO=False
                        if curSCROLL!=note.scroll:
                            if curline!="":
                                s+=curline+"\n"
                                curline=""
                            curSCROLL=note.scroll
                            s+="#SCROLL "+str(curSCROLL)+"\n"
                        curline+=str(note.noteParam)
                if curline!="":
                    s+=curline
                s+=",\n"
                curline=""
            s=s+"#END"+"\n"
        
        return s

    def __repr__(self):
        return str([self.TITLE,self.SUBTITLE,self.BPM,self.WAVE,self.SONGVOL,self.SEVOL,self.OFFSET,self.DEMOSTART,self.SIDE,self.SCOREMODE,self.GENRE,self.GAME,self.LIFE])


if __name__ == "__main__":
    # if len(sys.argv) < 2:
    #     sys.stderr.write("Usage: %s <rawData file>\n" % sys.argv[0])
    #     sys.exit(1)

    # fname = sys.argv[1]
    fname="test.tja"
    T=TJA(fname)
    T.print()