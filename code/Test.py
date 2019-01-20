import copy
class tst:
    def __init__(self):
        self.t=list()
    def setlist(self,t):
        self.t=t
    def setlistDeep(self,t):
        self.t=copy.deepcopy(t)
    def print(self):
        print(self.t)


t=[1,2,3]
tp=tst()
tp.setlist(t)
tp.print()
t=[2,3,4]
tp.print()
tp.setlistDeep(t)
t=[3,4,5]
tp.print()