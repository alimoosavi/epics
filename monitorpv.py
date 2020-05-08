from PyQt5.QtWidgets import QWidget, QApplication,QLabel,QVBoxLayout
from PyQt5.QtGui import QPainter, QColor, QBrush
from PyQt5.Qt import QRunnable, QThreadPool
from PyQt5.QtCore import pyqtSlot

import sys

import epics,time
from epics import Alarm, poll


class Worker(QRunnable):
    '''
    Worker thread
    '''
    def __init__(self, turn_on , turn_off, *args, **kwargs):

        super(Worker, self).__init__()

        self.turn_on = turn_on
        self.turn_off = turn_off

    @pyqtSlot()
    def run(self):

        switch_lamp_on_alarm = Alarm(pvname = 'pv.VAL',
                                     comparison = '>',
                                     callback = self.turn_on,
                                     trip_point = 50.0,
                                     )

        switch_lamp_off_alarm = Alarm(pvname = 'pv.VAL',
                                     comparison = '<=',
                                     callback = self.turn_off,
                                     trip_point = 50.0,
                                     )
        while True:
            poll()


class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.threadpool = QThreadPool()

        self.lamp_color = QColor(200, 0, 0)
        self.label = QLabel('good')
        self.initUI()
        self.monitor_pv()


    def turn_on_lamp(self , **kk):
        self.lamp_color = QColor(100, 10, 0)
        self.label.setText('bad')
        print ('ssss')
        self.update()

    def turn_off_lamp(self , **kk):
        self.lamp_color = QColor(200, 10, 0)
        self.label.setText('good')
        print ('lll')
        self.update()

    def monitor_pv(self):
        worker = Worker(self.turn_on_lamp , self.turn_off_lamp)
        self.threadpool.start(worker)


    def onChanges(self ,pvname=None, value=None, char_value=None, **kw):
        print (pvname , value)

    def initUI(self):

        layout = QVBoxLayout()
        layout.addWidget(self.label)

        self.setLayout(layout)

        self.show()



if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
