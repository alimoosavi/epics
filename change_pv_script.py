from PyQt5.QtWidgets import QWidget, QApplication,QLabel,QVBoxLayout
from PyQt5.Qt import QRunnable, QThreadPool
from PyQt5.QtCore import pyqtSlot
import random
import sys

import time
from epics import PV

p1 = PV('pv.VAL')

class Worker(QRunnable):
    '''
    Worker thread
    '''
    def __init__(self, temperature ,  set_temperature , *args, **kwargs):

        super(Worker, self).__init__()

        self.set_temperature = set_temperature
        self.temperature = temperature

    @pyqtSlot()
    def run(self):
        while True:
            self.temperature = random.randint(100, 150)
            self.set_temperature(self.temperature)
            time.sleep(1)


class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.threadpool = QThreadPool()

        self.temperature = 20
        self.label = QLabel(str(self.temperature))
        self.initUI()
        self.monitor_pv()


    def set_temperature(self , *kk):
        print(*kk)
        self.label.setText(str(*kk))
        self.update()


    def monitor_pv(self):
        worker = Worker(self.temperature , self.set_temperature)
        self.threadpool.start(worker)

    def initUI(self):

        layout = QVBoxLayout()
        layout.addWidget(self.label)

        self.setLayout(layout)

        self.show()



if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
