from PyQt5.QtWidgets import QWidget, QApplication,QLabel,QVBoxLayout
from PyQt5.Qt import QRunnable, QThreadPool
from PyQt5.QtCore import pyqtSlot
import random
import sys

import time
from epics import PV

temperature_pv_one = PV('temperature_one.VAL')
temperature_pv_two = PV('temperature_two.VAL')

temperature_default_value = 125

class Worker(QRunnable):
    '''
    Worker thread
    '''
    def __init__(self,   set_temperature_one , set_temperature_two , *args, **kwargs):

        super(Worker, self).__init__()

        self.set_temperature_one = set_temperature_one
        self.set_temperature_two = set_temperature_two

    @pyqtSlot()
    def run(self):
        while True:

            temp_rand = random.randint(100, 150)
            temperature_pv_one.put(value = temp_rand)
            self.set_temperature_one(temp_rand)


            temp_rand = random.randint(100, 150)
            temperature_pv_two.put(value = temp_rand)
            self.set_temperature_two(temp_rand)

            time.sleep(1)



class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.threadpool = QThreadPool()

        self.temperature_one_label = QLabel(str(temperature_default_value))
        self.temperature_two_label = QLabel(str(temperature_default_value))
        self.initUI()
        self.monitor_temperatures()


    def set_temperature_one(self , *kk):
        print("temperature one" , *kk)
        self.temperature_one_label.setText(str(*kk))
        self.update()

    def set_temperature_two(self , *kk):
        print("temperature two" , *kk)
        self.temperature_two_label.setText(str(*kk))
        self.update()


    def monitor_temperatures(self):
        worker = Worker(self.set_temperature_one , self.set_temperature_two)
        self.threadpool.start(worker)

    def initUI(self):

        layout = QVBoxLayout()
        layout.addWidget(self.temperature_one_label)
        layout.addWidget(self.temperature_two_label)

        self.setLayout(layout)

        self.show()



if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
