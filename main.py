# -*- coding: utf-8 -*-
import sys
import os, platform
import re
import subprocess
from PyQt4 import Qt, QtCore, QtGui, uic
import ctypes

form_class = uic.loadUiType("main.ui")[0]                 # Load the UI

class MainWindow(QtGui.QMainWindow, form_class):
    vpnserverip = "192.168.240"
    netmask = "255.255.255.0"
    gameServ = ["157.7.172.0","157.7.173.0","157.7.174.0"]
    res = subprocess.check_output(["ipconfig","/all"])
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        #self.setWindowFlags(Qt.Qt.FramelessWindowHint)
        self.setupUi(self)
        #self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)

        pal = self.palette()
        bg = pal.window().color()
        AERO_BACKGROUND_ALPHA = 250
        bg.setAlpha(AERO_BACKGROUND_ALPHA)
        pal.setColor(QtGui.QPalette.Window, bg)
        from ctypes import windll, c_int, byref
        windll.dwmapi.DwmExtendFrameIntoClientArea(c_int(self.winId()), byref(c_int(-1)))
        self.setPalette(pal)

        self.execBtn.clicked.connect(self.execBtn_clicked)
        self.urlable0.setOpenExternalLinks(True);
        self.urlable1.setOpenExternalLinks(True);
        osver = self.chechOS()
        self.pte.insertPlainText("[Check]作業系統為: %s\n\n".decode('utf8')%(osver))

    def execBtn_clicked(self):
            print self.rB1.isChecked()
            print self.rB2.isChecked()
            self.res = subprocess.check_output(["ipconfig","/all"])
            if self.rB1.isChecked():
                if self.VPNconnected():
                    self.pte.insertPlainText("[Check]VPN已連線!\n".decode('utf8'))
                    self.clearRoute()
                    if self.buildRoute():
                        self.pte.insertPlainText("FEZ網路設定已完成!\n\n".decode('utf8'))
                    else:
                        self.pte.insertPlainText("FEZ網路設定失敗!\n\n".decode('utf8'))
                        return False
                    return True
                else:
                    self.pte.insertPlainText(unicode("[Check] VPN未連線!\n\n".decode('utf8')))

            if self.rB2.isChecked():
                if self.clearRoute():
                    self.pte.insertPlainText("設定清除完成!\n\n".decode('utf8'))
                else:
                    self.pte.insertPlainText("設定清除完成!\n\n".decode('utf8'))
                return True

    def chechOS(self):
        if os.name == 'nt':
            return("%s%s"%(platform.system(),platform.release()))

    def VPNconnected(self):
        if self.res.find(self.vpnserverip) >= 0:
            return True
        else:
            return False

    def buildRoute(self):
        self.pte.insertPlainText("正在建立FEZ網路設定...\n".decode('utf8'))
        servip = self.findVPNserv()
        for gameservip in self.gameServ:
            subprocess.check_call("route add %s mask %s %s"%(gameservip,self.netmask,servip))
        return True

    def clearRoute(self):
        self.pte.insertPlainText("正在初始化FEZ網路設定...\n".decode('utf8'))
        for gameservip in self.gameServ:
            subprocess.check_call("route delete %s"%(gameservip))
        return True

    def findVPNserv(self):
        flag = re.compile('%s\.\d{1,3}'%(self.vpnserverip))
        servip = re.search(flag,self.res)
        return servip.group()




if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    mainWindow = MainWindow(None)
    mainWindow.show()
    app.exec_()