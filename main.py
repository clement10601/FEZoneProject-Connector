# -*- coding: utf-8 -*-
import sys
import os,platform
import shlex, subprocess
from PyQt4 import QtCore, QtGui, uic

form_class = uic.loadUiType("main.ui")[0]                 # Load the UI

class MainWindow(QtGui.QMainWindow, form_class):
    vpnserverip = "192.168.240"
    netmask = "255.255.255.0"
    gameServ = ["157.7.172.0","157.7.173.0","157.7.174.0"]
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.execBtn.clicked.connect(self.execBtn_clicked)
        osver = self.chechOS()
        self.pte.insertPlainText("OS: %s\n"%(osver))

    def execBtn_clicked(self):
            if self.rB1.toggled:
                if self.VPNconnected():
                    self.pte.insertPlainText("VPN已連線!\n".decode('utf8'))
                    self.clearRoute()
                    if self.buildRoute():
                        self.pte.insertPlainText("FEZ網路設定已完成\n".decode('utf8'))
                    else:
                        self.pte.insertPlainText("FEZ網路設定失敗\n".decode('utf8'))
                        return False
                    return True
                else:
                    self.pte.insertPlainText(unicode("錯誤: VPN未連線!\n".decode('utf8')))

            if self.rB2.toggled:
                if self.clearRoute():
                    self.pte.insertPlainText("初始化成功!\n".decode('utf8'))
                else:
                    self.pte.insertPlainText("已清除完成!\n".decode('utf8'))
                return True

    def chechOS(self):
        if os.name == 'nt':
            return("%s%s"%(platform.system(),platform.release()))

    def VPNconnected(self):
        res = subprocess.check_output(["ipconfig","/all"])
        if res.find(self.vpnserverip) >= 0:
            return True
        else:
            return False

    def buildRoute(self):
        self.pte.insertPlainText("正在建立FEZ網路設定...\n".decode('utf8'))
        return True

    def clearRoute(self):
        self.pte.insertPlainText("正在初始化FEZ網路設定...\n".decode('utf8'))
        return True


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    mainWindow = MainWindow(None)
    mainWindow.show()
    app.exec_()