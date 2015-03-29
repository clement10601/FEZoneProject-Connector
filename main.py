import sys
import shlex, subprocess
from PyQt4 import QtCore, QtGui, uic

form_class = uic.loadUiType("main.ui")[0]                 # Load the UI

class MainWindow(QtGui.QMainWindow, form_class):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.execBtn.clicked.connect(self.execBtn_clicked)

    def execBtn_clicked(self):
        print "exec"
        if self.rB1.toggled:
            print "rB1 checked"
            res = subprocess.check_output(["ipconfig"])
            print res
        elif self.rB2.toggled:
            print "rB2 checked"

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    mainWindow = MainWindow(None)
    mainWindow.show()
    app.exec_()