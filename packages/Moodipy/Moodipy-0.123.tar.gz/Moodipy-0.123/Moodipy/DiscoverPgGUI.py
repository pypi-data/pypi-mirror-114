from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from Moodipy.UserSummary import Person
from screeninfo import get_monitors
from Moodipy.PredictionGUI import PredictPG
from Moodipy.MoodAnalyzerGUI import MoodAnalyzerPg
from Moodipy.playlist_test import get_user_playlists


class DiscoverPG(QMainWindow):
    def __init__(self):
        max_screen_width = 1536
        min_screen_width = 1000

        max_screen_height = 864
        min_screen_height = 610
        super().__init__()
        self.title = "Discover Page"
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
        self.setStyleSheet("background-color:#fea493")
        self.mood_window()
        self.show()

    def mood_window(self):
        Person.setLabel(self, "Discover Page", False, self.sw * 43, self.sh * 20, self.sw * 370, self.sh * 50, self.sw * 30, "#fea493", True, 'Arial Rounded MT Bold')
        Person.setLabel(self, "", False, self.sw * 40, self.sh * 75, self.sw * 340, self.sh * 5, 0, "black", True , 'Consolas')

        self.popularBtn = QPushButton("   Discover the next hits!", self)
        self.popularBtn.setGeometry(self.sw * 43, self.sh * 120, self.sw * 700, self.sh * 120)
        self.popularBtn.setStyleSheet("background-color: #d88a7c; border-radius:25px;text-align: left;")
        self.popularBtn.setFont(QFont('Consolas', self.sw * 16))
        self.popularBtn.clicked.connect(self.on_popular)

        self.ownPlaylist = QPushButton("   Create Playlist From Your Own Public Playlist", self)
        self.ownPlaylist.setGeometry(self.sw * 43, self.sh * 420, self.sw * 700, self.sh * 120)
        self.ownPlaylist.setStyleSheet("background-color: #d88a7c; border-radius:25px;text-align: left;")
        self.ownPlaylist.setFont(QFont('Consolas', self.sw * 16))
        self.ownPlaylist.clicked.connect(self.on_ownPlay)

        self.playlistLikes = QPushButton("   Create Playlist From Your Liked Songs/Top Artists", self)
        self.playlistLikes.setGeometry(self.sw * 43, self.sh * 270, self.sw * 700, self.sh * 120)
        self.playlistLikes.setStyleSheet("background-color: #d88a7c; border-radius:25px;text-align: left;")
        self.playlistLikes.setFont(QFont('Consolas', self.sw * 16))
        self.playlistLikes.clicked.connect(self.on_likes)

    def on_popular(self):
        self.nextPg = PredictPG()
        self.nextPg.show()
        self.hide()

    def on_ownPlay(self):
        Person.choice = "playlist"
        playlists = get_user_playlists()
        if playlists == "NO PLAYLISTS":
            self.pop_up()
        elif playlists == None:
            self.pop_up2()
        else:
            Person.playlists = playlists
            self.nextPg = MoodAnalyzerPg()
            self.nextPg.show()
            self.hide()

    def on_likes(self):
        Person.choice = "likes"
        self.nextPg = MoodAnalyzerPg()
        self.nextPg.show()
        self.hide()

    def pop_up(self):
        msg = QMessageBox.question(self, 'Error', 'You have no public playlists, try adding some!', QMessageBox.Ok)

    def pop_up2(self):
        msg = QMessageBox.question(self, 'Error', 'Sorry, we have encountered a error. Try again later.', QMessageBox.Ok)
