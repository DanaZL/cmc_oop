#!/usr/bin/python
# simple.py

import sys
from PyQt5.QtWidgets import QWidget, QPushButton,QLineEdit,QInputDialog,QApplication
from designed_ui import Ui_DesignedWidget

app = QApplication(sys.argv)

# QtGui.QAp

widget = QWidget()
widget.resize(750, 650)
widget.setWindowTitle('simple')
widget.show()

sys.exit(app.exec_())