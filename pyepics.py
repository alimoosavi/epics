from epics import PV
p1 = PV('pv.VAL')
from epics import Alarm, poll


from PyQt5 import QtCore, QtGui, QtWidgets
import sys

class Ui_MainWindow(object):

    def setupUi(self, MainWindow):

        MainWindow.resize(550, 393)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.slider = QtWidgets.QSlider(self.centralwidget)
        self.slider.setGeometry(QtCore.QRect(190, 100, 400, 16))
        self.slider.setOrientation(QtCore.Qt.Horizontal)

       
        self.slider.sliderReleased.connect(self.valuechange)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(230, 150, 301, 161))

     
        self.font = QtGui.QFont()
        self.font.setPointSize(7)
        self.label.setFont(self.font)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def valuechange(self):
        p1.put(value = self.slider.value())

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "edit pv value"))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
