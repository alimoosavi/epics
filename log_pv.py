import mysql.connector
# from epics import Alarm, poll
import epics
import time

# mydb = mysql.connector.connect(
#   host="localhost",
#   user="root",
#   password="root"
# )
#
#
# mycursor = mydb.cursor()
#
# mycursor.execute("CREATE DATABASE epics")
#
# mycursor.execute("CREATE TABLE log_pvs (id INT AUTO_INCREMENT PRIMARY KEY , name VARCHAR(255), log VARCHAR(255))")
#
#


# import epics
def onChanges(pvname=None, value=None, char_value=None, **kw):
    f = open("pv.log", "a")
    f.write(pvname + " " + char_value + " " + time.ctime()+ "\n")
    f.close()
    # print('PV Changed! ', pvname, char_value, time.ctime())

pvname='pv'

mypv = epics.PV(pvname)
mypv.add_callback(onChanges)

print('Now wait for changes')

t0 = time.time()
while time.time() - t0 < 60.0:
    time.sleep(1.e-3)
print('Done.')


# fh = open('pv.log','w')
# while True:
#     epics.camonitor('pv.VAL',writer=fh.write)
#     fh.close()
# #
# Alarm(pvname = 'pv.VAL',
#                     comparison = '>',
#                     callback = self.turn_on,
#                             trip_point = 50.0,
#                              )
#
# while True:
#     poll()
#
# print(mydb)
