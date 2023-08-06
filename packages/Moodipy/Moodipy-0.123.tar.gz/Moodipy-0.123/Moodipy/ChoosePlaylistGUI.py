from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from Moodipy.UserSummary import Person
from Moodipy.PlaylistGUI import PlaylistPg
from screeninfo import get_monitors


class ChoosePlaylistPG(QMainWindow):
    def __init__(self):
        max_screen_width = 1536
        min_screen_width = 1000

        max_screen_height = 864
        min_screen_height = 610
        super().__init__()
        self.title = "Choose Playlist"
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
        self.setStyleSheet("background-color: #96bef0")
        self.currItem = None
        self.mood_window()
        self.show()

    def mood_window(self):
        title = QLabel("Choose A Playlist", self)
        title.setGeometry(self.sw*20, self.sh*10, self.sw*390, self.sh*45)
        title.setStyleSheet("background-color:#96bef0; font-weight: bold; color: white")
        title.setFont(QFont('Arial Rounded MT Bold', self.sw*30))

        Person.setLabel(self, "", False, 0, self.sh * 100, self.width, self.sh * 20, 0, "white", False, 'Segoe UI')

        Person.moodLabel = Person.setMoodLabel(Person, Person.currentmood)
        subtitle = QLabel("Base Your "+Person.moodLabel+" Playlist On The Songs In One Of Your Public Playlists", self)
        subtitle.setGeometry(self.sw * 21, self.sh * 60, self.sw * 999, self.sh * 30)
        subtitle.setStyleSheet("background-color:#96bef0; font-weight: bold; color: white")
        subtitle.setFont(QFont('Arial Rounded MT Bold', self.sw * 13))

        self.listWidget = QListWidget(self)
        self.listWidget.setGeometry(0, self.sh * 121, self.width, self.sh * 440)
        scrollBar = QScrollBar(self)
        self.listWidget.setVerticalScrollBar(scrollBar)
        self.listWidget.setStyleSheet("background-color: #96bef0;color: white")
        self.listWidget.itemSelectionChanged.connect(self.on_change)

        self.nextbtn = QPushButton("Create Playlist", self)
        self.nextbtn.setStyleSheet("background-color: #c2dcfb; font-weight: bold; border: 5px solid; border-color: #ebf3fb; hover { background-color : white}")
        self.nextbtn.setGeometry(self.sw * 620, self.sh * 565, self.sw * 180, self.sh * 40)
        self.nextbtn.clicked.connect(self.on_click)

        self.newbtn = QPushButton("Discover Page", self)
        self.newbtn.setStyleSheet("background-color: #c2dcfb; font-weight: bold; border: 5px solid; border-color: #ebf3fb; hover { background-color : white}")
        self.newbtn.setGeometry(self.sw * 200, self.sh * 565, self.sw * 180, self.sh * 40)
        self.newbtn.clicked.connect(self.on_click2)

        self.playlists = Person.playlists
        num = 1
        for playlist in self.playlists:
            if num < 10:
                playlistTitle = QListWidgetItem(str(num) + "     " + playlist)
            else:
                playlistTitle = QListWidgetItem(str(num) + "   " + playlist)

            playlistTitle.setFont(QFont('Arial Rounded MT Bold', self.sw * 20))
            self.listWidget.addItem(playlistTitle)
            num = num + 1

    def on_change(self):
        self.currItem = self.listWidget.selectedItems()
        self.currItem = str(self.currItem[0].text())
        num = self.listWidget.currentRow() + 1
        length = len(str(num))
        if num < 10:
            length = length + 5
        else:
            length = length + 3

        self.currItem = self.currItem[length:]

    def on_click2(self):
        from Moodipy.DiscoverPgGUI import DiscoverPG
        self.nextPg = DiscoverPG()
        self.nextPg.show()
        self.hide()
        
    def change_text(self):
        self.newbtn.setText("Please")
        self.nextbtn.setText("Wait...")
        
    def change_back(self):
        self.newbtn.setText("Discover Page")
        self.nextbtn.setText("Create Playlist")

    def on_click(self):
        from Moodipy.playlist_test import generate_playlist_from_another
        if self.currItem == None:
            self.pop_up()
        else:
            self.pop_up_wait()
            Person.tracks = generate_playlist_from_another(self.currItem, self.playlists)
            if Person.tracks == None:
                self.pop_up6()
            if Person.tracks == "ERROR NO SONGS" and len(self.playlists) > 1:
                self.pop_up2()
            elif Person.tracks == "ERROR NO SONGS":
                self.pop_up3()
            elif Person.tracks == "NO SONGS" and len(self.playlists) > 1:
                self.pop_up4()
            elif Person.tracks == "NO SONGS":
                self.pop_up5()
            else:
                self.nextPg = PlaylistPg()
                self.nextPg.show()
                self.hide()

        self.change_back()

    def pop_up(self):
        msg = QMessageBox.question(self, 'Error', 'Please select a playlist.', QMessageBox.Ok)

    def pop_up2(self):
        msg = QMessageBox.question(self, 'Error', 'There are no songs in the playlist you selected. Try adding some or choose another playlist!', QMessageBox.Ok)

    def pop_up3(self):
        msg = QMessageBox.question(self, 'Error', 'There are no songs in the playlist you selected. Try adding some or go back to the Discover Page!', QMessageBox.Ok)

    def pop_up4(self):
        msg = QMessageBox.question(self, 'Error', 'Hmm, we could not find any songs in the playlist that matches your mood, try selecting another playlist or go back to the Discover Page!', QMessageBox.Ok)

    def pop_up5(self):
        msg = QMessageBox.question(self, 'Error', 'Hmm, we could not find any songs in the playlist that matches your mood, try adding more songs/playlists or go back to the Discover Page!', QMessageBox.Ok)

    def pop_up6(self):
        msg = QMessageBox.question(self, 'Error', 'Sorry we encontered an Error. Please try again or go back to the Discovery Page.', QMessageBox.Ok)

    def pop_up_wait(self):
        self.change_text()
        msg = QMessageBox.question(self, 'Loading', 'Please wait while we generate your playlist! Press OK or exit this message to start!', QMessageBox.Ok)
