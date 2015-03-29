# Temperature-conversion program using PyQt

import sys
import os
from PyQt4 import QtCore, QtGui, uic

form_class = uic.loadUiType("main.ui")[0]                 # Load the UI

class MyWindowClass(QtGui.QMainWindow, form_class):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.execBtn.clicked.connect(self.execBtn_clicked)

    def execBtn_clicked(self):
        print "exec"
        if self.rB1.toggled:
            print "rB1 checked"
        elif self.rB2.toggled:
            print "rB2 checked"


app = QtGui.QApplication(sys.argv)
myWindow = MyWindowClass(None)
myWindow.show()
app.exec_()