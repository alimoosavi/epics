from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout, QMainWindow, QHBoxLayout
from PyQt5.Qt import QRunnable, QThreadPool
from PyQt5.QtCore import pyqtSlot
import random
import sys
import pyqtgraph as pg
import time
from epics import PV, Alarm, poll

temperature_pv_one = PV('temperature_one.VAL')
temperature_pv_two = PV('temperature_two.VAL')

temperature_default_value = 125


class Alarm_Worker(QRunnable):
    '''
    Worker thread
    '''

    def __init__(self, turn_on, turn_off, *args, **kwargs):
        super(Alarm_Worker, self).__init__()

        self.turn_on = turn_on
        self.turn_off = turn_off

    @pyqtSlot()
    def run(self):
        switch_lamp_on_alarm = Alarm(pvname='temperature_average.VAL',
                                     comparison='==',
                                     callback=self.turn_on,
                                     trip_point=1,
                                     )

        switch_lamp_off_alarm = Alarm(pvname='temperature_average.VAL',
                                      comparison='==',
                                      callback=self.turn_off,
                                      trip_point=0,
                                      )
        while True:
            poll()


class Worker(QRunnable):
    '''
    Worker thread
    '''

    def __init__(self, set_temperature_one, set_temperature_two, *args, **kwargs):
        super(Worker, self).__init__()

        self.set_temperature_one = set_temperature_one
        self.set_temperature_two = set_temperature_two

    @pyqtSlot()
    def run(self):
        while True:
            temp_rand = random.randint(100, 150)
            temperature_pv_one.put(value=temp_rand)
            self.set_temperature_one(temp_rand)

            temp_rand = random.randint(100, 150)
            temperature_pv_two.put(value=temp_rand)
            self.set_temperature_two(temp_rand)
            time.sleep(1)


class Example(QMainWindow):

    def __init__(self):
        super().__init__()

        self.graphWidget1 = pg.PlotWidget()
        self.graphWidget1.setBackground('w')

        pen1 = pg.mkPen(color=(255, 0, 0))

        self.graphWidget2 = pg.PlotWidget()
        self.graphWidget2.setBackground('w')

        pen2 = pg.mkPen(color=(255, 0, 0))

        self.setGeometry(60, 60, 1000, 1000)
        self.setWindowTitle('monitor temperatures')

        self.first_temperature_x = [1]
        self.second_temperature_x = [1]

        self.first_temperature_previous_records = [temperature_default_value]
        self.second_temperature_previous_records = [temperature_default_value]

        self.threadpool = QThreadPool()

        self.temperature_one_label = QLabel(str(temperature_default_value), self)
        self.temperature_two_label = QLabel(str(temperature_default_value), self)


        # moving position
        self.temperature_one_label.move(200, 200)
        self.temperature_two_label.move(500, 200)

        self.temperature_one_label.resize(200, 200)
        self.temperature_two_label.resize(200, 200)

        self.temperature_one_label.setStyleSheet("border: 3px solid blue; border-radius: 400 px;")
        self.temperature_two_label.setStyleSheet("border: 3px solid blue; border-radius: 400 px;")

        self.first_temperature_data_line = self.graphWidget1.plot(self.first_temperature_x,
                                                                  self.first_temperature_previous_records, pen=pen1)
        self.second_temperature_data_line = self.graphWidget2.plot(self.second_temperature_x,
                                                                   self.second_temperature_previous_records, pen=pen2)

        self.initUI()
        self.monitor_temperatures()

    def set_temperature_one(self, *first_temp):
        print("temperature one", *first_temp)

        self.first_temperature_x.append(self.first_temperature_x[-1] + 1)  # Add a new value 1 higher than the last.

        if len(self.first_temperature_previous_records) >= 6:
            self.first_temperature_previous_records = self.first_temperature_previous_records[1:]
            self.first_temperature_x = self.first_temperature_x[1:]  # Remove the first y element.

        self.first_temperature_previous_records.append(*first_temp)

        self.temperature_one_label.setText(str(*first_temp))
        print(self.first_temperature_x, self.first_temperature_previous_records)
        self.first_temperature_data_line.setData(self.first_temperature_x,
                                                 self.first_temperature_previous_records)  # Update the data.

    def set_temperature_two(self, *second_temp):
        print("temperature two", *second_temp)

        self.second_temperature_x.append(self.second_temperature_x[-1] + 1)  # Add a new value 1 higher than the last.

        if len(self.second_temperature_previous_records) >= 6:
            self.second_temperature_previous_records = self.second_temperature_previous_records[1:]
            self.second_temperature_x = self.second_temperature_x[1:]  # Remove the first y element.

        self.second_temperature_previous_records.append(*second_temp)

        self.temperature_two_label.setText(str(*second_temp))
        print(self.second_temperature_x, self.second_temperature_previous_records)
        self.second_temperature_data_line.setData(self.second_temperature_x,
                                                  self.second_temperature_previous_records)  # Update the data.

    def monitor_temperatures(self):

        worker = Worker(self.set_temperature_one, self.set_temperature_two)
        alarm_worker = Alarm_Worker(self.alarm_on, self.alarm_off)

        self.threadpool.start(worker)
        self.threadpool.start(alarm_worker)

    def alarm_on(self, **k):
        print('alarm on')

    def alarm_off(self , **k):
        print('alarm off')

    def initUI(self):
        ll = QVBoxLayout()

        ll1 = QVBoxLayout()
        ll2 = QVBoxLayout()

        layout = QHBoxLayout()
        layout.addSpacing(10)
        layout.addWidget(self.temperature_one_label)
        layout.addWidget(self.temperature_two_label)

        ll1.addWidget(self.graphWidget1)
        ll2.addWidget(self.graphWidget2)

        ll.addLayout(layout)
        ll.addLayout(ll1)
        ll.addLayout(ll2)
        widget = QWidget()
        widget.setLayout(ll)
        self.setCentralWidget(widget)

        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
