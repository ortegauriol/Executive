from PySide.QtCore import *
from PySide.QtGui import *
import sys
import socket
from socket import gethostname, gethostbyname
from ConfigParser import SafeConfigParser
import Dragonfly_config as rc
from PyDragonfly import Dragonfly_Module, CMessage, copy_to_msg,copy_from_msg
import datetime

import SynGui


class synergiesGUI(QMainWindow, SynGui.Ui_SynergiesGUI):
    # Constructor method

    def __init__(self, parent=None):
        super(synergiesGUI, self).__init__(parent)
        self.setupUi(self)

        # Button actions block
        self.connectButton.clicked.connect(self.check_host)
        self.ConnectHost = ConnectThread()

        # Widget Controller
        self.define_Button.clicked.connect(self.changePage)
        self.UR5_Button.clicked.connect(self.changePage)
        self.VR_Button.clicked.connect(self.changePage)

        #UR5 Buttons
        self.URNextButton.clicked.connect(self.ur5_command)

        #VR Feedback Buttons
        self.VRNextButton.clicked.connect(self.vr_command)


        #LABELS
        now = datetime.datetime.now()
        self.label_4.setText(now.strftime("%Y-%m-%d %H:%M"))

    # Button methods

    # Connect
    def check_host(self):
        if self.connectButton.isChecked():
            self.ConnectHost.start()
        else:
            self.ConnectHost.terminate()

    # Target Controller Widget
    def changePage(self):
        if self.define_Button.isChecked():
            self.stackedWidget.setCurrentIndex(1)
        elif self.VR_Button.isChecked():
            self.stackedWidget.setCurrentIndex(0)
        elif self.UR5_Button.isChecked():
            self.stackedWidget.setCurrentIndex(2)

    #UR5
    def ur5_command(self):
        # momentary commands to see that it works
        msg = CMessage(rc.MT_UR5_MOVEMENT_COMMAND)
        mdf = rc.MDF_UR5_MOVEMENT_COMMAND()
        pos = [0.33029437, -0.33029437, 0.3, 1.7599884, -0.72901107, 1.7599884]
        mdf.position[:] = pos[:]
        mdf.max_velocity = 1
        mdf.acceleration = 0.2
        copy_to_msg(mdf,msg)
        if self.connectButton.isChecked():
            mod = Dragonfly_Module(0, 0)
            mod.ConnectToMMM(('localhost:7111'))
            mod.SendModuleReady()
            mod.SendMessage(msg)
            print'Command Send'
            mod.DisconnectFromMMM()
        else:
            print 'Check Connect Button'

    def vr_command(self):
        # momentary commands to see that it works
        msg = CMessage(rc.MT_RTFT_CONFIG)
        mdf = rc.MDF_RTFT_CONFIG()
        target = [5, 10, -2]
        mdf.target_vector[:] = target[:]
        mdf.cursor_visible = True
        mdf.target_visible = True
        mdf.max_factor = 40
        copy_to_msg(mdf,msg)
        if self.connectButton.isChecked():
            mod = Dragonfly_Module(0, 0)
            mod.ConnectToMMM(('localhost:7111'))
            mod.SendModuleReady()
            mod.SendMessage(msg)
            print'Command Send'
            mod.DisconnectFromMMM()
        else:
            print 'Check Connect Button'




class ConnectThread(QThread):
    def __init__(self, parent=None):
        super(ConnectThread, self).__init__(parent)

    def run(self):
        print 'Connected to DragonFly!'
        mod = Dragonfly_Module(0,0)
        mod.ConnectToMMM(('localhost:7111'))
        mod.SendModuleReady()

    def terminate(self):
        mod = Dragonfly_Module(0,0)
        mod.DisconnectFromMMM()
        print 'Disconnected'



app = QApplication(sys.argv)
form = synergiesGUI()
form.show()
app.exec_()