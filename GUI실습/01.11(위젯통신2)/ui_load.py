import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *  # for QPixmap


form_class = uic.loadUiType("./ProjectTaiko/window_01_11.ui")[0]

class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.alpha_index = 1 # last alpha index
        self.measure = {'upper':4, 'lower':4}
        self.push_addBeta.clicked.connect(self.push_addBeta_clicked)
        self.push_removeBeta.clicked.connect(self.push_removeBeta_clicked)
        self.push_measure_setting.clicked.connect(self.push_measure_setting_clicked)
        
    def push_measure_setting_clicked(self):
        data = {'measureUpper':self.measure['upper'], 'measureLower':self.measure['lower']}
        dlg_measure = MeasureDialog(data)
        dlg_measure.exec_()
        if dlg_measure.apply == True:
            self.measure['upper'] = dlg_measure.measureUpper
            self.measure['lower'] = dlg_measure.measureLower
            self.label_measure.setText(str(self.measure['upper'])+' / '+str(self.measure['lower']))

    def push_addBeta_clicked(self):
        self.alpha_index += 1

        for i in range(self.measure['upper']-1):
            z = QLabel()
            z.setPixmap(QPixmap(':/track/res/beta(48x50).png'))
            bname = 'label_b'+str(self.alpha_index)+'_'+str(i) # index: 2_0, 2_1, ...
            z.setObjectName(bname)
            self.scrollLayout.addWidget(z)
        
        z = QLabel()
        z.setPixmap(QPixmap(':/track/res/beta_end(48x50).png'))
        bname = 'label_b'+str(self.alpha_index)+'_'+str(self.measure['upper']-1)
        z.setObjectName(bname)
        self.scrollLayout.addWidget(z)

    def push_removeBeta_clicked(self): # remove last beta
        count = 1+int(self.scrollLayout.itemAt(self.scrollLayout.count()-1).widget().objectName().split('_')[-1])
        for i in range(count):
            z = self.scrollLayout.takeAt(self.scrollLayout.count()-1) # QWidgetItem 타입 반환
            z.widget().deleteLater()
        self.alpha_index -= 1


measure_class = uic.loadUiType("./ProjectTaiko/dialog_01_11.ui")[0]

class MeasureDialog(QDialog, measure_class):
    def __init__(self, rdict):
        super().__init__()
        self.setupUi(self)
        self.apply = False
        self.measureUpper = rdict['measureUpper']
        self.measureLower = rdict['measureLower']
        self.spin_measure_upper.setValue(self.measureUpper)
        self.spin_measure_upper.valueChanged.connect(self.spin_measure_upper_valueChanged)
        self.combo_measure_lower.setCurrentIndex(self.combo_measure_lower.findText(str(self.measureLower)))
        self.combo_measure_lower.currentTextChanged.connect(self.combo_measure_lower_textChanged)
        self.push_apply.clicked.connect(self.push_apply_clicked)
        self.push_cancel.clicked.connect(self.push_cancel_clicked)

    def spin_measure_upper_valueChanged(self):
        self.measureUpper = self.spin_measure_upper.value()

    def combo_measure_lower_textChanged(self):
        self.measureLower = self.combo_measure_lower.currentText()

    def push_apply_clicked(self):
        self.apply = True
        self.close()

    def push_cancel_clicked(self):
        self.apply = False
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()