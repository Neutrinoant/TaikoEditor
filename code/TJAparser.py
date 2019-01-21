import re
import codecs
import Score
import sys


def delcomment(s):
    newstr=list()
    for i in s:
        if i=='':
            continue
        else:
            newstr.append(re.sub('//(.*)','',i))
    return newstr



def makeTrack(TJA):
    l=len(TJA)
    
    T=Score.TJA()
    T.Track_list.append(Score.Track())
    CurTrIdx=0
    CurBalloonlist=None
    flag=False
    bar=list()
    for line in range(l):
        if not flag:
            #곡 전체 데이터
            s=re.match('TITLE:(.*)',TJA[line])
            if s!=None:
                T.TITLE=s.group(1)
                continue
            s=re.match('SUBTITLE:(.*)',TJA[line])
            if s!=None:
                T.SUBTITLE=s.group(1)
                continue
            s=re.match('BPM:(.*)',TJA[line])
            if s!=None:
                T.BPM=int(s.group(1))
                continue
            s=re.match('WAVE:(.*)',TJA[line])
            if s!=None:
                T.WAVE=s.group(1)
                continue
            s=re.match('SONGVOL:(.*)',TJA[line])
            if s!=None:
                T.SONGVOL=int(s.group(1))
                continue
            s=re.match('SEVOL:(.*)',TJA[line])
            if s!=None:
                T.SEVOL=int(s.group(1))
                continue
            s=re.match('OFFSET:(.*)',TJA[line])
            if s!=None:
                T.OFFSET=float(s.group(1))
                continue
            s=re.match('DEMOSTART:(.*)',TJA[line])
            if s!=None:
                T.DEMOSTART=float(s.group(1))
                continue
            s=re.match('SIDE:(.*)',TJA[line])
            if s!=None:
                T.SIDE=int(s.group(1))
                continue
            s=re.match('SCOREMODE:(.*)',TJA[line])
            if s!=None:
                T.SCOREMODE=int(s.group(1))
                continue
            s=re.match('GENRE:(.*)',TJA[line])
            if s!=None:
                T.GENRE=s.group(1)
                continue

            #코스별 데이터
            s=re.match('COURSE:(.*)',TJA[line])
            if s!=None:
                T.Track_list[CurTrIdx].COURSE=s.group(1)
                # print(s.group(1))
                continue
            s=re.match('LEVEL:(.*)',TJA[line])
            if s!=None:
                T.Track_list[CurTrIdx].LEVEL=int(s.group(1))
                continue
            s=re.match('SCOREINIT:(.*)',TJA[line])
            if s!=None:
                if s.group(1) == '':
                    continue
                T.Track_list[CurTrIdx].SCOREINIT=int(s.group(1))
                continue
            s=re.match('SCOREDIFF:(.*)',TJA[line])
            if s!=None:
                if s.group(1) == '':
                    continue
                T.Track_list[CurTrIdx].SCOREDIFF=int(s.group(1))
                continue
            s=re.match('BALLOON:(.*)',TJA[line])
            if s!=None:
                if s.group(1) == '':
                    continue
                CurBalloonlist=s.group(1).split(',')
                # print(CurBalloonlist)
                continue
            s=re.match('STYLE:(.*)',TJA[line])
            if s!=None:
                if s.group(1) == '':
                    continue
                T.Track_list[CurTrIdx].STYLE=int(s.group(1))
                continue
            if TJA[line]=='#START':
                flag=True
        #보면 파싱하기
        else:
            if TJA[line]=='#END':
                flag=False
                T.Track_list[CurTrIdx].bar_list=makeBarList(bar,T.BPM,CurBalloonlist)
                bar=list()
                if line<l-1:
                    #END가 나오고 더 나오는게 있다면 일단 하나 더 만들기    
                    T.newTrack()
                    CurTrIdx=CurTrIdx+1
            else:
                bar=bar+[TJA[line]]
        
        
    T.print()
    
    return T

def makeBarList(bar,defaultBPM,Balloonlist):
    # print(bar)
    #이 함수는 bar의 list를 만든다. 
    res=list()
    curIdx=0
    SCROLL=1.0
    BalloonIdx=0
    BPM=defaultBPM
    GOGO=False
    MEASURE=[4,4]
    TempList=list()
    for line in bar:
        # print(line)
        if line[0]=='#':
            if line=='#GOGOSTART':
                GOGO=True
            if line=='#GOGOEND':
                GOGO=False
            s=re.match('#SCROLL (.*)',line)
            if s!=None:
                SCROLL=float(s.group(1))
                continue
            s=re.match('#BPMCHANGE (.*)',line)
            if s!=None:
                BPM=float(s.group(1))
                continue
            s=re.match("#MEASURE (.*)/(.*)",line)
            if s!=None:
                MEASURE[0]=int(s.group(1))
                MEASURE[1]=int(s.group(2))
                continue
        else:
            for note in line:
                if note==',':
                    if len(TempList)==0:
                        TempList.append(Score.Note(BPM,0,SCROLL,None,GOGO))
                    res.append(Score.Bar(MEASURE))
                    res[curIdx].setNoteList(TempList)
                    curIdx=curIdx+1
                    TempList=list()
                elif note=='7':
                    TempList.append(Score.Note(BPM,note,SCROLL,Balloonlist[BalloonIdx],GOGO))
                    BalloonIdx=BalloonIdx+1
                else:
                    TempList.append(Score.Note(BPM,note,SCROLL,None,GOGO))
    return res

if __name__ == "__main__":
    with codecs.open("../TJAfile/ドンカマ2000.tja", "r",encoding='shift-jis', errors='ignore') as f:
        dat=f.read()
        s=dat.splitlines()
        # print(s)

    s=delcomment(s)
    # print(s)
    makeTrack(s)





    