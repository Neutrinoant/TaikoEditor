import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *  # for QPixmap


form_class = uic.loadUiType("./ProjectTaiko/window_01_07.ui")[0]

class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.label_betaList = []
        self.alpha_index = 1 # last alpha index
        self.measure = {'upper':4, 'lower':4}
        self.push_addBeta.clicked.connect(self.push_addBeta_clicked)
        self.push_removeBeta.clicked.connect(self.push_removeBeta_clicked)
        self.spin_upper.valueChanged.connect(self.spin_upper_changed)
        self.spin_lower.valueChanged.connect(self.spin_lower_changed)
        

    def push_addBeta_clicked(self):
        self.alpha_index += 1

        for i in range(self.measure['upper']-1):
            z = QLabel()
            z.setPixmap(QPixmap(':/track/res/beta(48x50).png'))
            bname = 'label_b'+str(self.alpha_index)+'_'+str(i) # index: 2_0, 2_1, ...
            z.setObjectName(bname)
            self.scrollLayout.addWidget(z)
            #print(bname + ' added')
        
        z = QLabel()
        z.setPixmap(QPixmap(':/track/res/beta_end(48x50).png'))
        bname = 'label_b'+str(self.alpha_index)+'_'+str(self.measure['upper']-1)
        z.setObjectName(bname)
        self.scrollLayout.addWidget(z)
        #print(bname + ' added')
        

    def push_removeBeta_clicked(self): # remove last beta
        count = 1+int(self.scrollLayout.itemAt(self.scrollLayout.count()-1).widget().objectName().split('_')[-1])
        for i in range(count):
            z = self.scrollLayout.takeAt(self.scrollLayout.count()-1) # QWidgetItem 타입 반환
            #print(z.widget().objectName() + ' removed')
            z.widget().deleteLater()
        self.alpha_index -= 1

    def spin_upper_changed(self):
        self.measure['upper'] = self.spin_upper.value()

    def spin_lower_changed(self):
        self.measure['lower'] = self.spin_lower.value()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()