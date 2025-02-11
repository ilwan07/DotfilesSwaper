import PyQt5.QtWidgets as qtw
from PyQt5 import QtGui, QtCore


class VSeparator(qtw.QFrame):
    def __init__(self):
        super().__init__()
        self.setFrameShape(qtw.QFrame.VLine)
        self.setFrameShadow(qtw.QFrame.Sunken)
