from screeninfo import get_monitors
from Moodipy.ChoosePlaylistGUI import ChoosePlaylistPG
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from Moodipy.moodAnalyzer import find_mood
from Moodipy.UserSummary import Person
from Moodipy.LoadPage import LoadPg
from os import path

class MoodAnalyzerPg(QMainWindow):
    def __init__(self):
        max_screen_width = 1536
        min_screen_width = 1000

        max_screen_height = 864
        min_screen_height = 610
        super().__init__()
        self.title = "Mood Analyzer"
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
        self.setStyleSheet("background-color:#abbdff")
        self.mood_window()
        self.show()

    def mood_window(self):
        # Labels
        Person.setLabel(self,"How are you feeling?", False, self.sw*20, self.sh*10, self.sw*370, self.sh*39, self.sw*20, "#abbdff", True, 'Segoe UI')
        Person.setLabel(self,"Write about your day...", False, self.sw*120, self.sh*70, self.sw*300, self.sh*35, self.sw*15, "#abbdff", False, 'Segoe UI')
        Person.setLabel(self, "Find your mood", False, self.sw*670, self.sh*70, self.sw*300, self.sh*35, self.sw*15, "#abbdff", False, 'Segoe UI')
        Person.setLabel(self, "", False, self.sw*20, self.sh*58, self.sw*320, self.sh*3, 0, "black", False, 'Segoe UI')
        # Textbox
        self.text = QTextEdit(self)
        self.text.setGeometry(self.sw*60, self.sh*100, self.sw*350, self.sh*450)
        self.text.setStyleSheet("border: 30px solid; border-radius:60px; background-color: #99acff; border-color: #99acff")
        self.text.setFont(QFont('Segoe UI', self.sw*11))
        # Block design
        boxDesign = QLabel(self)
        boxDesign.setGeometry(self.sw*570, self.sh*100, self.sw*350, self.sh*450)
        boxDesign.setStyleSheet("border: 30px solid; border-radius:60px; background-color: #99acff; border-color: #99acff")
        # OR label

        orLabel = QLabel("OR", self)
        orLabel.setAlignment(Qt.AlignCenter)
        orLabel.setGeometry(self.sw*460, self.sh*300, self.sw*60, self.sh*60)
        orLabel.setStyleSheet("border-radius: 30px; background-color: #99acff; border-color: #99acff; font-weight: bold")
        orLabel.setFont(QFont('Segoe UI', self.sw*12))


        # Text submit button
        btn1 = QPushButton("submit", self)
        btn1.clicked.connect(self.on_click)
        btn1.setGeometry(self.sw*200, self.sh*500, self.sw*80, self.sh*20)
        btn1.setStyleSheet("background-color: #abbdff;border-radius:10px; ")
        
        #awful image/btn
        awful_img = QLabel(self)
        awful_img.setGeometry(self.sw*630, self.sh*130, self.sw*90, self.sh*90)
        currMood = path.join(path.join(path.dirname(__file__), "imgs"), "awful.jpeg")
        awful_img.setStyleSheet("border-image : url(%s);" % currMood)
        self.awful_btn = QPushButton("awful", self)
        self.awful_btn.setGeometry(self.sw*645, self.sh*225, self.sw*65, self.sh*20)
        self.awful_btn.setStyleSheet("background-color: #99acff; font-weight: bold; border-radius:10px;")
        self.awful_btn.setFont(QFont('Segoe UI', self.sw * 11))
        self.awful_btn.clicked.connect(self.on_awful)
        
        #bad image/btn
        bad_img = QLabel(self)
        bad_img.setGeometry(self.sw*780, self.sh*130, self.sw*90, self.sh*90)
        currMood = path.join(path.join(path.dirname(__file__), "imgs"), "bad.jpeg")
        bad_img.setStyleSheet("border-image : url(%s);" % currMood)
        self.bad_btn = QPushButton("bad", self)
        self.bad_btn.setGeometry(self.sw*793, self.sh*225, self.sw*65, self.sh*20)
        self.bad_btn.setStyleSheet("background-color: #99acff; font-weight: bold; border-radius:10px;")
        self.bad_btn.setFont(QFont('Segoe UI', self.sw*11))
        self.bad_btn.clicked.connect(self.on_bad)
        
        #okay image/btn
        okay_img = QLabel(self)
        okay_img.setGeometry(self.sw*630, self.sh*260, self.sw*90, self.sh*90)
        currMood = path.join(path.join(path.dirname(__file__), "imgs"), "okay.jpeg")
        okay_img.setStyleSheet("border-image : url(%s);" % currMood)
        self.okay_btn = QPushButton("okay", self)
        self.okay_btn.setGeometry(self.sw*645, self.sh*355, self.sw*65, self.sh*20)
        self.okay_btn.setStyleSheet("background-color: #99acff; font-weight: bold; border-radius:10px;")
        self.okay_btn.setFont(QFont('Segoe UI', self.sw * 11))
        self.okay_btn.clicked.connect(self.on_okay)
        
        #happy image/btn
        happy_img = QLabel(self)
        happy_img.setGeometry(self.sw*780, self.sh*260, self.sw*90, self.sh*90)
        currMood = path.join(path.join(path.dirname(__file__), "imgs"), "happy.jpeg")
        happy_img.setStyleSheet("border-image : url(%s);" % currMood)
        self.happy_btn = QPushButton("happy", self)
        self.happy_btn.setGeometry(self.sw*795, self.sh*355, self.sw*65, self.sh*20)
        self.happy_btn.setStyleSheet("background-color: #99acff; font-weight: bold; border-radius:10px;")
        self.happy_btn.setFont(QFont('Segoe UI', self.sw*11))
        self.happy_btn.clicked.connect(self.on_happy)
        
        #excited image/btn
        excited_img = QLabel(self)
        excited_img.setGeometry(self.sw*630, self.sh*380, self.sw*90, self.sh*90)
        currMood = path.join(path.join(path.dirname(__file__), "imgs"), "excited.jpeg")
        excited_img.setStyleSheet("border-image : url(%s);" % currMood)
        self.excited_btn = QPushButton("excited", self)
        self.excited_btn.setGeometry(self.sw*640, self.sh*475, self.sw*70, self.sh*20)
        self.excited_btn.setStyleSheet("background-color: #99acff; font-weight: bold; border-radius:10px;")
        self.excited_btn.setFont(QFont('Segoe UI', self.sw * 11))
        self.excited_btn.clicked.connect(self.on_excited)
        
        #love image/btn
        love_img = QLabel(self)
        love_img.setGeometry(self.sw*780, self.sh*380, self.sw*90, self.sh*90)
        currMood = path.join(path.join(path.dirname(__file__), "imgs"), "love.jpeg")
        love_img.setStyleSheet("border-image : url(%s);" % currMood)
        self.love_btn = QPushButton("love", self)
        self.love_btn.setGeometry(self.sw*790, self.sh*475, self.sw*65, self.sh*20)
        self.love_btn.setStyleSheet("background-color: #99acff; font-weight: bold; border-radius:10px;")
        self.love_btn.setFont(QFont('Segoe UI', self.sw * 11))
        self.love_btn.clicked.connect(self.on_love)
        
        # Mood submit button
        btn2 = QPushButton("submit", self)
        btn2.clicked.connect(self.on_click2)
        btn2.setGeometry(self.sw*720, self.sh*500, self.sw*80, self.sh*20)
        btn2.setStyleSheet("background-color: #abbdff;border-radius:10px; ")

    def on_click(self):
        Person.currentmood = find_mood(self.text.toPlainText())
        if Person.currentmood is None:
            print("Please be more descriptive")
            self.pop_up()
        else:
            if Person.choice == "likes":
                self.nextPg = LoadPg()
                self.nextPg.show()
                self.hide()
            elif Person.choice == "playlist":
                self.nextPg = ChoosePlaylistPG()
                self.nextPg.show()
                self.hide()

    def pop_up(self):
        msg = QMessageBox.question(self, 'Error', 'Please be more descriptive', QMessageBox.Ok)
    
    def pop_up2(self):
        msg = QMessageBox.question(self, 'Error', 'Please select a mood', QMessageBox.Ok)


    def on_click2(self):
        if self.selected_mood is None:
            self.pop_up2()
        else:
            mood = []
            mood.append(self.selected_mood)
            Person.currentmood = mood
            if Person.choice == "likes":
                self.nextPg = LoadPg()
                self.nextPg.show()
                self.hide()
            elif Person.choice == "playlist":
                self.nextPg = ChoosePlaylistPG()
                self.nextPg.show()
                self.hide()
    
    def on_happy(self):
        self.selected_mood = "happy"
        self.happy_btn.setStyleSheet("background-color: #abbdff; font-weight: bold; border-radius:10px;")
        self.awful_btn.setStyleSheet("background-color: #99acff; font-weight: bold; border-radius:10px;")
        self.bad_btn.setStyleSheet("background-color: #99acff; font-weight: bold; border-radius:10px;")
        self.okay_btn.setStyleSheet("background-color: #99acff; font-weight: bold; border-radius:10px;")
        self.excited_btn.setStyleSheet("background-color: #99acff; font-weight: bold; border-radius:10px;")
        self.love_btn.setStyleSheet("background-color: #99acff; font-weight: bold; border-radius:10px;")

    def on_awful(self):
        self.selected_mood = "awful"
        self.awful_btn.setStyleSheet("background-color: #abbdff; font-weight: bold; border-radius:10px;")
        self.happy_btn.setStyleSheet("background-color: #99acff; font-weight: bold; border-radius:10px;")
        self.bad_btn.setStyleSheet("background-color: #99acff; font-weight: bold; border-radius:10px;")
        self.okay_btn.setStyleSheet("background-color: #99acff; font-weight: bold; border-radius:10px;")
        self.excited_btn.setStyleSheet("background-color: #99acff; font-weight: bold; border-radius:10px;")
        self.love_btn.setStyleSheet("background-color: #99acff; font-weight: bold; border-radius:10px;")

    def on_bad(self):
        self.selected_mood = "bad"
        self.bad_btn.setStyleSheet("background-color: #abbdff; font-weight: bold; border-radius:10px;")
        self.happy_btn.setStyleSheet("background-color: #99acff; font-weight: bold; border-radius:10px;")
        self.awful_btn.setStyleSheet("background-color: #99acff; font-weight: bold; border-radius:10px;")
        self.okay_btn.setStyleSheet("background-color: #99acff; font-weight: bold; border-radius:10px;")
        self.excited_btn.setStyleSheet("background-color: #99acff; font-weight: bold; border-radius:10px;")
        self.love_btn.setStyleSheet("background-color: #99acff; font-weight: bold; border-radius:10px;")

    def on_okay(self):
        self.selected_mood = "okay"
        self.okay_btn.setStyleSheet("background-color: #abbdff; font-weight: bold; border-radius:10px;")
        self.happy_btn.setStyleSheet("background-color: #99acff; font-weight: bold; border-radius:10px;")
        self.bad_btn.setStyleSheet("background-color: #99acff; font-weight: bold; border-radius:10px;")
        self.awful_btn.setStyleSheet("background-color: #99acff; font-weight: bold; border-radius:10px;")
        self.excited_btn.setStyleSheet("background-color: #99acff; font-weight: bold; border-radius:10px;")
        self.love_btn.setStyleSheet("background-color: #99acff; font-weight: bold; border-radius:10px;")

    def on_excited(self):
        self.selected_mood = "excited"
        self.excited_btn.setStyleSheet("background-color: #abbdff; font-weight: bold; border-radius:10px;")
        self.happy_btn.setStyleSheet("background-color: #99acff; font-weight: bold; border-radius:10px;")
        self.bad_btn.setStyleSheet("background-color: #99acff; font-weight: bold; border-radius:10px;")
        self.awful_btn.setStyleSheet("background-color: #99acff; font-weight: bold; border-radius:10px;")
        self.okay_btn.setStyleSheet("background-color: #99acff; font-weight: bold; border-radius:10px;")
        self.love_btn.setStyleSheet("background-color: #99acff; font-weight: bold; border-radius:10px;")

    def on_love(self):
        self.selected_mood = "love"
        self.love_btn.setStyleSheet("background-color: #abbdff; font-weight: bold; border-radius:10px;")
        self.happy_btn.setStyleSheet("background-color: #99acff; font-weight: bold; border-radius:10px;")
        self.bad_btn.setStyleSheet("background-color: #99acff; font-weight: bold; border-radius:10px;")
        self.awful_btn.setStyleSheet("background-color: #99acff; font-weight: bold; border-radius:10px;")
        self.okay_btn.setStyleSheet("background-color: #99acff; font-weight: bold; border-radius:10px;")
        self.excited_btn.setStyleSheet("background-color: #99acff; font-weight: bold; border-radius:10px;")

