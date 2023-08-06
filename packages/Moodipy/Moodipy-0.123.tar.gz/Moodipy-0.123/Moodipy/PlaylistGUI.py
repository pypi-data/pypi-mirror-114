from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from Moodipy.UserSummary import Person
from screeninfo import get_monitors

class PlaylistPg(QMainWindow):
    def __init__(self):
        max_screen_width = 1536
        min_screen_width = 1000

        max_screen_height = 864
        min_screen_height = 610
        super().__init__()
        self.title = "Playlist"
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
        self.setStyleSheet(
            "background-color:qlineargradient(spread:pad, x1:0, y1:1, x2:0, y2:0, stop:0 rgba(208, 255, 244, 255), stop:0.00507614 rgba(208, 255, 244, 255), stop:0.664865 rgba(208, 255, 244, 255), stop:0.666667 rgba(151, 223, 201, 255), stop:1 rgba(161, 223, 204, 255))")
        self.mood_window()
        self.show()

    def mood_window(self):
        # Generate another playlist btn
        nextbtn = QPushButton("Discover Page...", self)
        nextbtn.setStyleSheet("background-color:rgba(208, 255, 244, 255); font-weight: bold; border: 5px solid; border-color:white")
        nextbtn.setGeometry(self.sw*800, self.sh*20, self.sw*180, self.sh*30)
        nextbtn.clicked.connect(self.on_click)
        # Creates a playlist name
        Person.playlistName = Person.setPlaylistName(Person, Person.moodLabel, Person.currentmood)
        Person.setLabel(self, Person.playlistName, False, self.sw * 350, self.sh * 80, self.sw * 520, self.sh * 58, self.sw * 30, "rgba(161, 223, 204, 255)", True, "Segoe UI")
        # Tracks List Widget
        listWidget = QListWidget(self)
        listWidget.setGeometry(0, self.sh*200, self.width, self.sh*410)
        scrollBar = QScrollBar(self)
        listWidget.setVerticalScrollBar(scrollBar)
        listWidget.setStyleSheet("background-color:rgba(208, 255, 244, 255); ")

        tracks = Person.tracks
        # Add tracks to list widget
        num = 1
        for song, title in tracks.items():
            if num < 10:
                songtitle = QListWidgetItem(str(num) + "     " + song)
            else:
                songtitle = QListWidgetItem(str(num) + "   " + song)
            artist = QListWidgetItem("               " + title + "\n")
            songtitle.setFont(QFont("Segoe UI", self.sw * 20))
            artist.setFont(QFont("Segoe UI", self.sw * 10))
            listWidget.addItem(songtitle)
            listWidget.addItem(artist)
            num = num + 1
    # Add another Mood
    def on_click(self):
        from Moodipy.DiscoverPgGUI import DiscoverPG
        self.nextPg = DiscoverPG()
        self.nextPg.show()
        self.hide()

