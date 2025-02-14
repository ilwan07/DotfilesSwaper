from widgets import *
import PyQt5.QtWidgets as qtw
from PyQt5 import QtGui, QtCore
from pathlib import Path
import platformdirs
import shutil
import json
import glob
import sys


class MainWindow(qtw.QMainWindow):
    def __init__(self):
        super().__init__()

        # some variables
        self.nbColumns = 3

        # basic setup
        self.appdataDir = Path(platformdirs.user_data_dir("DotfilesSwapper", appauthor="Ilwan"))
        self.appdataDir.mkdir(parents=True, exist_ok=True)
        self.profilesDir = self.appdataDir / "profiles"
        self.profilesDir.mkdir(parents=True, exist_ok=True)

        self.settingsFile = self.appdataDir / "settings.json"
        if not self.settingsFile.exists():
            self.writeSettings(default=True)
            createDefault = True
        else:
            createDefault = False
            with open(self.settingsFile, "r", encoding="utf-8") as f:
                self.settings = json.load(f)

        # main interface
        self.mainWidget = qtw.QWidget()
        self.setCentralWidget(self.mainWidget)
        self.mainLayout = qtw.QVBoxLayout()
        self.mainWidget.setLayout(self.mainLayout)

        self.createHeader()
        self.createGrid()
        self.setupInterface()

        if createDefault:
            self.newProfile(name="default")
    
    def createHeader(self):
        """build the UI for the header, with a few buttons and options"""
        # basic structure
        self.headerWidget = qtw.QWidget()
        self.headerLayout = qtw.QHBoxLayout()
        self.headerWidget.setLayout(self.headerLayout)
        self.mainLayout.addWidget(self.headerWidget)

        # create the widgets
        self.newProfileButton = qtw.QPushButton("New profile")
        self.newProfileButton.setFixedHeight(40)
        self.newProfileButton.setFont(QtGui.QFont("Arial", 14))
        self.newProfileButton.clicked.connect(self.newProfile)
        self.headerLayout.addWidget(self.newProfileButton)

        self.headerLayout.addWidget(VSeparator())

        self.dotfilesPath = qtw.QLineEdit()
        self.dotfilesPath.setPlaceholderText("dotfiles folder path")
        self.dotfilesPath.setReadOnly(True)
        self.dotfilesPath.setFixedHeight(40)
        self.dotfilesPath.setMinimumWidth(200)
        self.dotfilesPath.setFont(QtGui.QFont("Arial", 14))
        self.headerLayout.addWidget(self.dotfilesPath)

        self.dotfilesPathButton = qtw.QPushButton()
        self.dotfilesPathButton.setIcon(QtGui.QIcon("assets/folder.png"))
        self.dotfilesPathButton.setIconSize(QtCore.QSize(30, 30))
        self.dotfilesPathButton.setFixedSize(40, 40)
        self.dotfilesPathButton.clicked.connect(self.chooseDotfilesPath)
        self.headerLayout.addWidget(self.dotfilesPathButton)

        self.resetdotfilesPathButton = qtw.QPushButton()
        self.resetdotfilesPathButton.setIcon(QtGui.QIcon("assets/reset.png"))
        self.resetdotfilesPathButton.setIconSize(QtCore.QSize(30, 30))
        self.resetdotfilesPathButton.setFixedSize(40, 40)
        self.resetdotfilesPathButton.clicked.connect(self.resetDotfilesPath)
        self.headerLayout.addWidget(self.resetdotfilesPathButton)

        self.headerLayout.addWidget(VSeparator())

        self.browseProfiles = qtw.QPushButton("Browse profile files")
        self.browseProfiles.setFixedHeight(40)
        self.browseProfiles.setFont(QtGui.QFont("Arial", 14))
        self.browseProfiles.clicked.connect(self.openProfileFiles)
        self.headerLayout.addWidget(self.browseProfiles)

    def createGrid(self):
        """build the UI for the scrollable main grid, with the list of dotfiles profiles"""
        # basic structure with a scrollable area
        self.gridScroll = qtw.QScrollArea()
        self.gridScroll.setWidgetResizable(True)
        self.gridScroll.setFrameShape(qtw.QFrame.NoFrame)
        self.gridScrollWidget = qtw.QWidget()
        self.gridScrollLayout = qtw.QGridLayout(self.gridScrollWidget)
        self.gridScrollLayout.setAlignment(QtCore.Qt.AlignTop)
        self.gridScroll.setWidget(self.gridScrollWidget)
        self.mainLayout.addWidget(self.gridScroll, 1)

    def setupInterface(self):
        """set up the interface with the proper values and items"""
        # set the dotfiles path
        self.dotfilesPath.setText(self.settings["dotfilesPath"])

        # load the profiles in the grid
        self.displayProfiles()
    
    def displayProfiles(self):
        """load the profiles in the grid, removes the previous ones if needed"""
        # remove the previous profiles
        for i in reversed(range(self.gridScrollLayout.count())):
            widget = self.gridScrollLayout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        # load the profiles
        profiles = sorted(glob.glob(str(self.profilesDir / "*")))
        for i, profile in enumerate(profiles):
            profilePath = Path(profile)
            profileName = profilePath.name

            with open(profilePath / "properties.json", "r", encoding="utf-8") as f:
                properties = json.load(f)
            profileWidget = profileDisplay(profileName)
            profileWidget.profileDescription.setText(properties["description"])

            if (profilePath / "banner.png").exists():
                bannerPath = str(profilePath / "banner.png")
            else:
                bannerPath = "assets/banner.png"
            pixmap = QtGui.QPixmap(bannerPath)
            scaledPixmap = pixmap.scaled(profileWidget.profileBanner.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
            profileWidget.profileBanner.setPixmap(scaledPixmap)

            profileWidget.edit.connect(self.editProfile)
            profileWidget.delete.connect(self.deleteProfile)
            profileWidget.load.connect(self.loadProfile)

            self.gridScrollLayout.addWidget(profileWidget, i // self.nbColumns, i % self.nbColumns)

    def writeSettings(self, default:bool=False):
        """write the default settings to the settings file and load them"""
        if default:
            self.settings = {
                "dotfilesPath": str(Path.home() / ".config"),
            }
        with open(self.settingsFile, "w", encoding="utf-8") as f:
            json.dump(self.settings, f, indent=4)

    def chooseDotfilesPath(self):
        """open a file dialog to choose the dotfiles folder path"""
        folder = qtw.QFileDialog.getExistingDirectory(self, "Select Dotfiles Folder", str(Path.home()))
        if folder:
            self.settings["dotfilesPath"] = folder
            self.writeSettings()
            self.dotfilesPath.setText(self.settings["dotfilesPath"])

    def resetDotfilesPath(self):
        """reset the dotfiles folder path to the default value"""
        self.settings["dotfilesPath"] = str(Path.home() / ".config")
        self.writeSettings()
        self.dotfilesPath.setText(self.settings["dotfilesPath"])

    def openProfileFiles(self):
        """open the folder containing the profile files"""
        QtCore.QProcess.startDetached("xdg-open", [str(self.profilesDir)])
    
    def newProfile(self, name:str=None):
        """create a new profile"""
        if not name:
            name, ok = qtw.QInputDialog.getText(self, "New profile", "Enter the name of the new profile:")
            if not ok:
                return
            if not name:
                return
            if "/" in name:
                qtw.QMessageBox.critical(self, "Error", "The profile name cannot contain the '/' character.")
                return

        profilePath = self.profilesDir / name
        if profilePath.exists():
            qtw.QMessageBox.critical(self, "Error", "A profile with this name already exists.")
            return
        profilePath.mkdir(parents=True)
        
        description, ok = qtw.QInputDialog.getText(self, "New profile", "Enter a short profile description:")
        if not ok:
            description = ""

        profileProperties = {
            "name": name,
            "description": description,
        }
        with open(profilePath / "properties.json", "w", encoding="utf-8") as f:
            json.dump(profileProperties, f, indent=4)
        
        bannerPath = qtw.QFileDialog.getOpenFileName(self, "Select profile banner image", str(Path.home()), "Images (*.png *.jpg *.jpeg)")[0]
        if bannerPath:
            shutil.copy2(bannerPath, profilePath / "banner.png")
        else:
            shutil.copy2("assets/banner.png", profilePath / "banner.png")
        
        profileDotfilesPath = profilePath / "dotfiles"
        profileDotfilesPath.mkdir()
        dotfilesPath = Path(self.settings["dotfilesPath"])
        if dotfilesPath.exists() and dotfilesPath.is_dir():
            for item in dotfilesPath.iterdir():
                dest = profileDotfilesPath / item.name
                if item.is_dir():
                    try:
                        shutil.copytree(item, dest)
                    except Exception as e:
                        print(f"Exception while copying the '{str(item)}' dir: {e}")
                else:
                    try:
                        shutil.copy2(item, dest)
                    except Exception as e:
                        print(f"Exception while copying the '{str(item)}' file: {e}")
            self.displayProfiles()
        else:
            qtw.QMessageBox.critical(self, "Dotfiles folder error", "The given dotfiles folder is invalid. Check that the folder exists.")

    def editProfile(self, name:str):
        """edit the properties of a profile"""
        pass  #TODO

    def deleteProfile(self, name:str):
        """delete a profile"""
        confirm = qtw.QMessageBox.warning(self, "Delete profile", f"Do you really want to delete '{name}'?", qtw.QMessageBox.Yes | qtw.QMessageBox.No)
        if confirm == qtw.QMessageBox.Yes:
            profilePath = self.profilesDir / name
            shutil.rmtree(profilePath)
            self.displayProfiles()
    
    def loadProfile(self, name:str):
        """load a profile"""
        pass #TODO


def setDarkMode(App:qtw.QApplication):
    """sets the app to a dark mode palette"""
    palette = QtGui.QPalette()
    palette.setColor(QtGui.QPalette.Window, QtGui.QColor(53, 53, 53))
    palette.setColor(QtGui.QPalette.WindowText, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.Base, QtGui.QColor(25, 25, 25))
    palette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(53, 53, 53))
    palette.setColor(QtGui.QPalette.ToolTipBase, QtCore.Qt.black)
    palette.setColor(QtGui.QPalette.ToolTipText, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.Text, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.Button, QtGui.QColor(53, 53, 53))
    palette.setColor(QtGui.QPalette.ButtonText, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.BrightText, QtCore.Qt.red)
    palette.setColor(QtGui.QPalette.Link, QtGui.QColor(42, 130, 218))
    palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(42, 130, 218))
    palette.setColor(QtGui.QPalette.HighlightedText, QtCore.Qt.black)
    App.setPalette(palette)


if __name__ == "__main__":
    App = qtw.QApplication(sys.argv)
    setDarkMode(App)
    Window = MainWindow()
    Window.setWindowTitle("Dotfiles swapper")
    Window.show()
    sys.exit(App.exec_())
