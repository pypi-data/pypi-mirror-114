import sys
import os.path

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMessageBox

import schoolschedulerapp.schedulerui as schedulerui
from schoolschedulerapp.schedule import *
from schoolschedulerapp.wsl import *
from schoolschedulerapp.generatedata import *

class SchoolScheduler(QtWidgets.QMainWindow, schedulerui.Ui_MainWindow):
    def __init__(self, parent=None):
        super(SchoolScheduler, self).__init__(parent)
        self.setupUi(self)


def start_gui():

    app = QApplication(sys.argv)
    form = SchoolScheduler()
    form.show()
    app.exec_()



def main():
    db_purge()
    db_init()

    # UI
    set_display_to_host()

    start_gui()



if __name__ == '__main__':
    main()
