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
    load = QtCore.pyqtSignal(str)

    def __init__(self, name):
        super().__init__()
        self.name = name

        self.mainLayout = qtw.QVBoxLayout()
        self.mainLayout.setAlignment(QtCore.Qt.AlignCenter)
        self.setLayout(self.mainLayout)

        # profile name
        self.profileName = qtw.QLabel(self.name)
        self.profileName.setFont(QtGui.QFont("Arial", 16))
        self.profileName.setWordWrap(True)
        self.profileName.setAlignment(QtCore.Qt.AlignCenter)
        self.mainLayout.addWidget(self.profileName)

        # profile banner image
        self.profileBanner = qtw.QLabel()
        self.profileBanner.setMaximumWidth(300)
        self.profileBanner.setFixedHeight(200)
        self.profileBanner.setAlignment(QtCore.Qt.AlignCenter)
        self.mainLayout.addWidget(self.profileBanner)

        # profile description
        self.profileDescription = qtw.QLabel()
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

        self.editButton = qtw.QPushButton("Edit")
        self.editButton.setFixedHeight(40)
        self.editButton.setFont(QtGui.QFont("Arial", 14))
        self.editButton.clicked.connect(lambda: self.edit.emit(self.name))
        self.buttonsLayout.addWidget(self.editButton)

        self.deleteButton = qtw.QPushButton("Delete")
        self.deleteButton.setFixedHeight(40)
        self.deleteButton.setFont(QtGui.QFont("Arial", 14))
        self.deleteButton.clicked.connect(lambda: self.delete.emit(self.name))
        self.buttonsLayout.addWidget(self.deleteButton)

        self.loadButton = qtw.QPushButton("Load profile")
        self.loadButton.setFixedHeight(45)
        self.loadButton.setFont(QtGui.QFont("Arial", 16))
        self.loadButton.clicked.connect(lambda: self.load.emit(self.name))
        self.mainLayout.addWidget(self.loadButton)


class profileEdit(qtw.QDialog):
    save = QtCore.pyqtSignal(str, str, str, str)

    def __init__(self, name: str, banner: str, description: str):
        super().__init__()
        self.name = name
        self.banner = banner
        self.description = description

        self.setWindowTitle("Edit Profile")
        self.setModal(True)

        self.mainLayout = qtw.QVBoxLayout()
        self.mainLayout.setAlignment(QtCore.Qt.AlignCenter)
        self.setLayout(self.mainLayout)

        # profile name
        self.profileName = qtw.QLineEdit(self.name)
        self.profileName.setFixedHeight(40)
        self.profileName.setPlaceholderText("Profile name")
        self.profileName.setFont(QtGui.QFont("Arial", 16))
        self.profileName.setAlignment(QtCore.Qt.AlignCenter)
        self.mainLayout.addWidget(self.profileName)

        # profile banner image
        self.profileBanner = qtw.QLabel()
        pixmap = QtGui.QPixmap(self.banner)
        scaled_pixmap = pixmap.scaledToHeight(100, QtCore.Qt.SmoothTransformation)
        self.profileBanner.setPixmap(scaled_pixmap)
        self.profileBanner.setAlignment(QtCore.Qt.AlignCenter)
        self.profileBanner.setFixedHeight(100)
        self.mainLayout.addWidget(self.profileBanner)

        # profile description
        self.profileDescription = qtw.QTextEdit(self.description)
        self.profileDescription.setPlaceholderText("Profile description")
        self.profileDescription.setFont(QtGui.QFont("Arial", 12))
        self.profileDescription.setAlignment(QtCore.Qt.AlignCenter)
        self.mainLayout.addWidget(self.profileDescription)

        # profile banner
        self.bannerButton = qtw.QPushButton("Change banner")
        self.bannerButton.setFixedHeight(40)
        self.bannerButton.setFont(QtGui.QFont("Arial", 14))
        self.bannerButton.clicked.connect(self.changeBanner)
        self.mainLayout.addWidget(self.bannerButton)

        # save button
        self.saveButton = qtw.QPushButton("Save")
        self.saveButton.setFixedHeight(40)
        self.saveButton.setFont(QtGui.QFont("Arial", 14))
        self.saveButton.clicked.connect(self.saveProfile)
        self.mainLayout.addWidget(self.saveButton)

    def changeBanner(self):
        newBanner = qtw.QFileDialog.getOpenFileName(self, "Select banner image", QtCore.QDir.homePath(), "Images (*.png *.jpg *.jpeg)")[0]
        if newBanner:
            self.banner = newBanner
            self.profileBanner.setPixmap(QtGui.QPixmap(self.banner))

    def saveProfile(self):
        self.save.emit(self.name, self.profileName.text(), self.banner, self.profileDescription.toPlainText())
        self.accept()


class flexGridWidget(qtw.QWidget):
    def __init__(self):
        """a widget that will hold a scrollable grid which will will adapt the number of columns to the available space on each resize"""
        super().__init__()
        pass  #TODO
