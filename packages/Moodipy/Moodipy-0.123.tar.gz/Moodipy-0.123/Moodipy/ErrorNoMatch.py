from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from Moodipy.UserSummary import Person
from screeninfo import get_monitors
from Moodipy.playlist_test import get_user_playlists

class ErrorNoSongs(QMainWindow):
    def __init__(self):
        max_screen_width = 1536
        min_screen_width = 1000

        max_screen_height = 864
        min_screen_height = 610
        super().__init__()
        self.title = "Error"
        self.desktop = QApplication.desktop()
        self.left = 0
        self.top = 0
        temp_width = get_monitors()[0].width * .5
        self.width = max(min(temp_width, max_screen_width), min_screen_width)
        temp_height = get_monitors()[0].height * .5
        self.height = max(min(temp_height, max_screen_height), min_screen_height)
        self.selected_mood = None
        self.initUI()

    def initUI(self):
        self.sw = (self.width / 1000)
        self.sh = (self.height / 610)
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.setStyleSheet("background-color:#ffcce6")
        self.mood_window()
        self.show()

    def mood_window(self):
        back = QLabel(self)
        back.setGeometry(self.sw * 100, self.sh * 150, self.sw * 800, self.sh * 300)
        back.setStyleSheet("background-color: #ffe0ff;border-radius:10px;")
        Person.setLabel(self, "Hmmm, It seems no songs in your", True, self.sw * 130, self.sh * 200, self.sw * 740, self.sh * 50, self.sw * 25, "#ffe0ff", True, 'Segoe UI')
        Person.setLabel(self, "Library match your mood.", True, self.sw*130, self.sh*300, self.sw*740, self.sh*50, self.sw*25, "#ffe0ff", True, 'Segoe UI')

        self.tryAgainBtn = QPushButton("Try Selecting Your Own Playlist", self)
        self.tryAgainBtn.setGeometry(self.sw * 310, self.sh * 480, self.sw * 400, self.sh * 30)
        self.tryAgainBtn.setStyleSheet("background-color: #ffe0ff; font-weight: bold; border-radius:10px;")
        self.tryAgainBtn.setFont(QFont('Segoe UI', self.sw * 14))
        self.tryAgainBtn.clicked.connect(self.on_tryAgain)

        self.newBtn = QPushButton("Discover Page", self)
        self.newBtn.setGeometry(self.sw * 310, self.sh * 520, self.sw * 400, self.sh * 30)
        self.newBtn.setStyleSheet("background-color: #ffe0ff; font-weight: bold; border-radius:10px;")
        self.newBtn.setFont(QFont('Segoe UI', self.sw * 14))
        self.newBtn.clicked.connect(self.on_new)

    def on_new(self):
        from Moodipy.DiscoverPgGUI import DiscoverPG
        self.nextPg = DiscoverPG()
        self.nextPg.show()
        self.hide()

    def on_tryAgain(self):
        from Moodipy.ChoosePlaylistGUI import ChoosePlaylistPG
        Person.choice = "playlist"
        playlists = get_user_playlists()
        if playlists == "NO PLAYLISTS":
            self.pop_up()
        elif playlists == None:
            self.pop_up2()
        else:
            Person.playlists = playlists
            self.nextPg = ChoosePlaylistPG()
            self.nextPg.show()
            self.hide()

    def pop_up(self):
        msg = QMessageBox.question(self, 'Error', 'You have no public playlists, try adding some!', QMessageBox.Ok)

    def pop_up2(self):
        msg = QMessageBox.question(self, 'Error', 'Sorry, we have encountered a error. Please Try again later.', QMessageBox.Ok)
