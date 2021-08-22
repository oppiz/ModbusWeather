from PyQt5 import QtCore, QtGui, QtWidgets
from pyModbusTCP.client import ModbusClient
from PyQt5.QtCore import QTime, QTimer
from time import strftime
import sys
import struct

import subprocess


#Take to 16bit to a 32 bit
def two16To32(first, second):
    words = [first, second]
    packed_string = struct.pack("HH", *words)
    unpacked_float = struct.unpack("f", packed_string)[0]
    return unpacked_float


SERVER_HOST = "192.168.2.250"
SERVER_PORT = 502

c = ModbusClient()

# uncomment this line to see debug message
#c.debug(True)

# define modbus server host, port
c.host(SERVER_HOST)
c.port(SERVER_PORT)


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(800, 460)
        Form.setWindowTitle("Form")

        self.timer = QTimer()
        self.timer.timeout.connect(self.showTime)
        self.timer.start(1000)

        self.timer2 = QTimer()
        self.timer2.timeout.connect(self.TempHumidUpdate)
        self.timer2.start(30000)
        
        self.Clock = QtWidgets.QLCDNumber(Form)
        self.Clock.setGeometry(QtCore.QRect(180, 20, 451, 201))
        self.Clock.setObjectName("Clock")


        self.lcdTemp = QtWidgets.QLCDNumber(Form)
        self.lcdTemp.setGeometry(QtCore.QRect(70, 250, 250, 125))
        self.lcdTemp.setObjectName("lcdTemp")

        self.lcdHumid = QtWidgets.QLCDNumber(Form)
        self.lcdHumid.setGeometry(QtCore.QRect(470, 250, 250, 125))
        self.lcdHumid.setObjectName("lcdHumid")

        self.Close_Button = QtWidgets.QPushButton("Close", Form)
        self.Close_Button.setGeometry(QtCore.QRect(710, 440, 75, 23))
        self.Close_Button.setObjectName("Close")

        self.label = QtWidgets.QLabel("Temperature", Form)
        self.label.setGeometry(QtCore.QRect(120, 370, 131, 41))

        font = QtGui.QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setFrameShadow(QtWidgets.QFrame.Raised)
        self.label.setScaledContents(False)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.label.setObjectName("label")

        self.label_2 = QtWidgets.QLabel("Humidity", Form)
        self.label_2.setGeometry(QtCore.QRect(550, 370, 101, 41))
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.label_2.setObjectName("label_2")

        QtCore.QMetaObject.connectSlotsByName(Form)

        self.TempHumidUpdate()


    def showTime(self):
        #Blink the middle? This code does that
        #time = QTime.currentTime()
        #text = time.toString('hh:mm')
        #if (time.second() % 2) == 0:
        #    text = text[:2] + ' ' + text[3:]

        #self.Clock.display(text)
        #24 hour time
        self.Clock.display(strftime("%H"+":"+"%M"))
        #12 hour time
        self.Clock.display(strftime("%I"+":"+"%M"))

    def TempHumidUpdate(self):
        if not c.is_open():
            if not c.open():
                print("unable to connect to "+SERVER_HOST+":"+str(SERVER_PORT))

        # if open() is ok, read register (modbus function 0x03)
        if c.is_open():
            regs4 = c.read_holding_registers(28672, 8)
            # if success display registers
            if regs4:  
                Temp = int(two16To32(regs4[0], regs4[1]))
                Humid = int(two16To32(regs4[2], regs4[3]))
                    
                self.lcdTemp.display(Temp)
                self.lcdHumid.display(Humid)

                #print(Temp)
                #print(Humid)
          
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    c.close()
    sys.exit(app.exec_())
 