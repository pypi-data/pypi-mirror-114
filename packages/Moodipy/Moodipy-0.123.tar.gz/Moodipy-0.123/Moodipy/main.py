import sys
import os
from os import path
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from Moodipy.UserSummary import Person
from Moodipy.UserLogin import UserLoginPG
from screeninfo import get_monitors
from Moodipy.DiscoverPgGUI import DiscoverPG


class MainWindow(QMainWindow):
    def __init__(self):
        max_screen_width = 1536
        min_screen_width = 1000

        max_screen_height = 864
        min_screen_height = 610
        super().__init__()
        self.title = "Moodipy"
        self.desktop = QApplication.desktop()
        self.left = 0
        self.top = 0
        temp_width = get_monitors()[0].width * .5
        self.width = max(min(temp_width, max_screen_width), min_screen_width)
        temp_height = get_monitors()[0].height * .5
        self.height = max(min(temp_height, max_screen_height), min_screen_height)
        self.initUI()


    def initUI(self):
        self.sw = (self.width / 1000)
        self.sh = (self.height / 610)
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.setStyleSheet("background-color: #ffdb94")
        self.main_window()
        self.show()

    def main_window(self):
        button = QPushButton(self)
        button.setGeometry(self.sw*480, self.sh*450, self.sw*40, self.sh*20)
        arrow_img = path.join(path.join(path.dirname(__file__), "imgs"), "arrow.png")
        styleS = "border-image : url(" + arrow_img + ");"
        button.setStyleSheet(styleS)
        button.clicked.connect(self.nextPG)

        Person.setLabel(self, "Welcome to", True, self.sw*390, self.sh*200, self.sw*220, self.sh*35, self.sw*19, "white", False,'Consolas')
        Person.setLabel(self, "Moodipy", True, self.sw*380, self.sh*260, self.sw*230, self.sh*58, self.sw*35, "white", True, 'Segoe UI')
        Person.setLabel(self, "Generating playlists that express how you feel", True, self.sw*335, self.sh*375, self.sw*338, self.sh*20, self.sw*9, "white", False,'Consolas')

    def paintEvent(self, event):
        paint = QPainter(self)
        paint.setPen(QPen(Qt.white, 5, Qt.SolidLine))
        paint.setBrush(QBrush(Qt.white, Qt.SolidPattern))
        paint.drawEllipse(self.sw*270, self.sh*70, self.sw*450, self.sh*450)

    def nextPG(self):
        userInfoPath = path.join(path.dirname(__file__), "UserInfo.txt")
        if os.path.isfile(userInfoPath):
            if os.stat(userInfoPath).st_size == 0:
                self.nextPG = UserLoginPG()
                self.nextPG.show()
                self.hide()
            f = open(userInfoPath, "r+")
            Person.userID = f.readline()
            f.close()
            self.nextPG = DiscoverPG()
            self.nextPG.show()
            self.hide()
        else:
            self.nextPG = UserLoginPG()
            self.nextPG.show()
            self.hide()

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
