from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from Moodipy.UserSummary import Person
from screeninfo import get_monitors

class PredictPG(QMainWindow):
    def __init__(self):
        max_screen_width = 1536
        min_screen_width = 1000

        max_screen_height = 864
        min_screen_height = 610
        super().__init__()
        self.title = "Popular Prediction"
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
        self.setStyleSheet("background-color:#b198f9")
        self.mood_window()
        self.show()

    def mood_window(self):
        title = QLabel("Next Trending Songs", self)
        title.setGeometry(self.sw * 20, self.sh * 10, self.sw * 420, self.sh * 45)
        title.setStyleSheet("background-color:#b198f9; font-weight: bold; color: white")
        title.setFont(QFont('Arial Rounded MT Bold', self.sw * 25))
        Person.setLabel(self, "", False, self.sw * 20, self.sh * 60, self.sw * 400, self.sh * 6, 0, "white", False, 'Segoe UI')

        self.newbtn = QPushButton("Discover Page", self)
        self.newbtn.setStyleSheet("background-color: #a88cf8; font-weight: bold; border: 5px solid; border-color: #ebf3fb; color: white")
        self.newbtn.setGeometry(self.sw * 420, self.sh * 565, self.sw * 180, self.sh * 40)
        self.newbtn.clicked.connect(self.on_click2)

        listWidget = QListWidget(self)
        listWidget.setGeometry(0, self.sh * 69, self.width, self.sh * 490)
        scrollBar = QScrollBar(self)
        listWidget.setVerticalScrollBar(scrollBar)
        listWidget.setStyleSheet("background-color:#b198f9; color: white ")
        
        #Just Test Tracks
        tracks = {"Song1":"Artist 1", "Song2":"Artist 2", "Song3":"Artist 3", "Song4":"Artist 4","Song5":"Artist 5", "Song6":"Artist 6", "Song7":"Artist 7", "Song8":"Artist 8","Song9":"Artist 9", "Song10":"Artist 10", "Song11":"Artist 11", "Song12":"Artist 12"}
       
        num = 1
        for song, title in tracks.items():
            if num < 10:
                songtitle = QListWidgetItem(str(num) + "     " + song)
            else:
                songtitle = QListWidgetItem(str(num) + "   " + song)
            artist = QListWidgetItem("               " + title + "\n")
            songtitle.setFont(QFont("Arial Rounded MT Bold", self.sw * 20))
            artist.setFont(QFont("Arial Rounded MT Bold", self.sw * 10))
            listWidget.addItem(songtitle)
            listWidget.addItem(artist)
            num = num + 1

    def on_click2(self):
        from Moodipy.DiscoverPgGUI import DiscoverPG
        self.nextPg = DiscoverPG()
        self.nextPg.show()
        self.hide()
