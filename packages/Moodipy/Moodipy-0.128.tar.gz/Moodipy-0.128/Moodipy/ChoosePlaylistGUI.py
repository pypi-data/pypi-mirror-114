from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from Moodipy.UserSummary import Person
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
        title = QLabel("Choose Up To Three Playlists", self)
        title.setGeometry(self.sw*20, self.sh*10, self.sw*690, self.sh*45)
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
        self.listWidget.itemSelectionChanged.connect(self.check_selection)
        self.listWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.listWidget.setStyleSheet("background-color: #96bef0;color: white")
        self.listWidget.itemSelectionChanged.connect(self.on_change)

        self.nextbtn = QPushButton("Create Playlist", self)
        self.nextbtn.setStyleSheet("background-color: #c2dcfb; font-weight: bold; border: 5px solid; border-color: #ebf3fb; hover { background-color : white}")
        self.nextbtn.setGeometry(self.sw * 620, self.sh * 565, self.sw * 180, self.sh * 40)
        self.nextbtn.clicked.connect(self.on_click)

        self.backbtn = QPushButton("Go Back", self)
        self.backbtn.setStyleSheet("background-color: #c2dcfb; font-weight: bold; border: 5px solid; border-color: #ebf3fb; hover { background-color : white}")
        self.backbtn.setGeometry(self.sw * 200, self.sh * 565, self.sw * 180, self.sh * 40)
        self.backbtn.clicked.connect(self.on_click2)

        self.newbtn = QPushButton("Discover Page", self)
        self.newbtn.setStyleSheet("background-color: #c2dcfb; font-weight: bold; border: 5px solid; border-color: #ebf3fb; hover { background-color : white}")
        self.newbtn.setGeometry(self.sw*800, self.sh*20, self.sw*180, self.sh*30)
        self.newbtn.clicked.connect(self.on_click3)

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
    
    def check_selection(self):
        items = self.listWidget.selectedItems()
        if len(items) > 3:
            items[0].setSelected(False)

    def on_change(self):
        self.currItem = self.listWidget.selectedItems()
        rows = self.listWidget.selectedIndexes()
        currItems = self.currItem
        names = []
        for i, item in enumerate(currItems):
            curr = str(item.text())
            num = rows[i].row() + 1
            length = len(str(num))
            if num < 10:
                length = length + 5
            else:
                length = length + 3
            curr = curr[length:]
            names.append(curr)

        Person.playlistNames = names

    def on_click2(self):
        from Moodipy.MoodAnalyzerGUI import MoodAnalyzerPg
        self.nextbtn.setEnabled(False)
        self.backbtn.setEnabled(False)
        self.newbtn.setEnabled(False)
        self.nextPg = MoodAnalyzerPg()
        self.nextPg.show()
        self.hide()
        
    def on_click3(self):
        from Moodipy.DiscoverPgGUI import DiscoverPG
        self.nextbtn.setEnabled(False)
        self.backbtn.setEnabled(False)
        self.newbtn.setEnabled(False)
        self.nextPg = DiscoverPG()
        self.nextPg.show()
        self.hide()
        

    def on_click(self):
        self.nextbtn.setEnabled(False)
        self.backbtn.setEnabled(False)
        self.newbtn.setEnabled(False)
        if self.currItem == None:
            self.pop_up()
        else:
            from Moodipy.LoadChoiceGUI import LoadChoicePg
            self.nextPg = LoadChoicePg()
            self.nextPg.show()
            self.hide()


    def pop_up(self):
        msg = QMessageBox.question(self, 'Error', 'Please select a playlist.', QMessageBox.Ok)
        self.nextbtn.setEnabled(True)
        self.backbtn.setEnabled(True)
        self.newbtn.setEnabled(True)
