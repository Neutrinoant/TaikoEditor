import re
import codecs
import Score
import sys

class rawDataparser:
    def __init__(self,fname):
        with codecs.open(fname, "r", encoding='shift-jis', errors='ignore') as f:
        self.rawData=delcomment(f.read().splitlines())
        s=dat.splitlines()
        self.s=delcomment(s)
        t=makeTrack(s)
        return t


    def delcomment(s):
        newStr=list()
        for i in s:
            if i=='':
                continue
            else:
                newStr.append(re.sub('//(.*)','',i))
        return newStr



    def makeTrack(rawData):
        l=len(rawData)
        
        T.track_list.append(Score.Track())
        curTrIdx=0
        curBalloonList=None
        flag=False
        bar=list()
        for line in range(l):
            if not flag:
                #곡 전체 데이터
                s=re.match('TITLE:(.*)',rawData[line])
                if s!=None:
                    T.TITLE=s.group(1)
                    continue
                s=re.match('SUBTITLE:(.*)',rawData[line])
                if s!=None:
                    T.SUBTITLE=s.group(1)
                    continue
                s=re.match('BPM:(.*)',rawData[line])
                if s!=None:
                    T.BPM=int(s.group(1))
                    continue
                s=re.match('WAVE:(.*)',rawData[line])
                if s!=None:
                    T.WAVE=s.group(1)
                    continue
                s=re.match('SONGVOL:(.*)',rawData[line])
                if s!=None:
                    T.SONGVOL=int(s.group(1))
                    continue
                s=re.match('SEVOL:(.*)',rawData[line])
                if s!=None:
                    T.SEVOL=int(s.group(1))
                    continue
                s=re.match('OFFSET:(.*)',rawData[line])
                if s!=None:
                    T.OFFSET=float(s.group(1))
                    continue
                s=re.match('DEMOSTART:(.*)',rawData[line])
                if s!=None:
                    T.DEMOSTART=float(s.group(1))
                    continue
                s=re.match('SIDE:(.*)',rawData[line])
                if s!=None:
                    T.SIDE=int(s.group(1))
                    continue
                s=re.match('SCOREMODE:(.*)',rawData[line])
                if s!=None:
                    T.SCOREMODE=int(s.group(1))
                    continue
                s=re.match('GENRE:(.*)',rawData[line])
                if s!=None:
                    T.GENRE=s.group(1)
                    continue

                #코스별 데이터
                s=re.match('COURSE:(.*)',rawData[line])
                if s!=None:
                    T.track_list[curTrIdx].COURSE=s.group(1)
                    # print(s.group(1))
                    continue
                s=re.match('LEVEL:(.*)',rawData[line])
                if s!=None:
                    T.track_list[curTrIdx].LEVEL=int(s.group(1))
                    continue
                s=re.match('SCOREINIT:(.*)',rawData[line])
                if s!=None:
                    if s.group(1) == '':
                        continue
                    T.track_list[curTrIdx].SCOREINIT=int(s.group(1))
                    continue
                s=re.match('SCOREDIFF:(.*)',rawData[line])
                if s!=None:
                    if s.group(1) == '':
                        continue
                    T.track_list[curTrIdx].SCOREDIFF=int(s.group(1))
                    continue
                s=re.match('BALLOON:(.*)',rawData[line])
                if s!=None:
                    if s.group(1) == '':
                        continue
                    curBalloonList=s.group(1).split(',')
                    # print(curBalloonList)
                    continue
                s=re.match('STYLE:(.*)',rawData[line])
                if s!=None:
                    if s.group(1) == '':
                        continue
                    T.track_list[curTrIdx].STYLE=s.group(1)
                    continue
                if rawData[line]=='#START':
                    flag=True
            #보면 파싱하기
            else:
                if rawData[line]=='#END':
                    flag=False
                    T.track_list[curTrIdx].bar_list=makeBarList(bar,T.BPM,curBalloonList)
                    bar=list()
                    if line<l-1:
                        #END가 나오고 더 나오는게 있다면 일단 하나 더 만들기    
                        T.newTrack()
                        curTrIdx=curTrIdx+1
                else:
                    bar=bar+[rawData[line]]
            
        print(T.torawDataForm())
        return T


    def makeBarList(bar,defaultBPM,balloonList):
        # print(bar)
        #이 함수는 bar의 list를 만든다. 
        res=list()
        curIdx=0
        SCROLL=1.0
        balloonIdx=0
        BPM=defaultBPM
        GOGO=False
        MEASURE=[4,4]
        tempList=list()
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
                        if len(tempList)==0:
                            tempList.append(Score.Note(BPM,0,SCROLL,None,GOGO))
                        res.append(Score.Bar(MEASURE))
                        res[curIdx].setNoteList(tempList)
                        curIdx=curIdx+1
                        tempList=list()
                    elif note=='7':
                        tempList.append(Score.Note(BPM,note,SCROLL,balloonList[balloonIdx],GOGO))
                        balloonIdx=balloonIdx+1
                    else:
                        tempList.append(Score.Note(BPM,note,SCROLL,None,GOGO))
        return res


def rawDataparser(fname):
    


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.stderr.write("Usage: %s <rawData file>\n" % sys.argv[0])
        sys.exit(1)

    fname = sys.argv[1]
    rawDataparser(fname)
