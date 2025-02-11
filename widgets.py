import PyQt5.QtWidgets as qtw
from PyQt5 import QtGui, QtCore


class VSeparator(qtw.QFrame):
    def __init__(self):
        super().__init__()
        self.setFrameShape(qtw.QFrame.VLine)
        self.setFrameShadow(qtw.QFrame.Sunken)


class profileDisplay(qtw.QWidget):
    edit = QtCore.pyqtSignal(str)
    delete = QtCore.pyqtSignal(str)

    def __init__(self, name):
        super().__init__()
        self.name = name

        self.mainLayout = qtw.QVBoxLayout()
        self.mainLayout.setAlignment(QtCore.Qt.AlignCenter)
        self.setLayout(self.mainLayout)

        # profile name
        self.profileName = qtw.QLabel(self.name)
        self.profileName.setFont(QtGui.QFont("Arial", 16))
        self.profileName.setAlignment(QtCore.Qt.AlignCenter)
        self.mainLayout.addWidget(self.profileName)

        # profile banner image
        self.profileBanner = qtw.QLabel()
        self.profileBanner.setMaximumWidth(300)
        self.profileBanner.setFixedHeight(200)
        self.profileBanner.setAlignment(QtCore.Qt.AlignCenter)
        self.mainLayout.addWidget(self.profileBanner)

        # profile description
        self.profileDescription = qtw.QLabel("[profile description]")
        self.profileDescription.setFont(QtGui.QFont("Arial", 12))
        self.profileDescription.setWordWrap(True)
        self.profileDescription.setAlignment(QtCore.Qt.AlignCenter)
        self.mainLayout.addWidget(self.profileDescription)

        # profile buttons
        self.buttonsWidget = qtw.QWidget()
        self.buttonsLayout = qtw.QHBoxLayout()
        self.buttonsLayout.setAlignment(QtCore.Qt.AlignCenter)
        self.buttonsWidget.setLayout(self.buttonsLayout)
        self.mainLayout.addWidget(self.buttonsWidget)

        self.editButton = qtw.QPushButton("Edit properties")
        self.editButton.setFixedHeight(40)
        self.editButton.setFont(QtGui.QFont("Arial", 14))
        self.editButton.clicked.connect(lambda: self.edit.emit(self.name))
        self.buttonsLayout.addWidget(self.editButton)

        self.deleteButton = qtw.QPushButton("Delete profile")
        self.deleteButton.setFixedHeight(40)
        self.deleteButton.setFont(QtGui.QFont("Arial", 14))
        self.deleteButton.clicked.connect(lambda: self.delete.emit(self.name))
        self.buttonsLayout.addWidget(self.deleteButton)
