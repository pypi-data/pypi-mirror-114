# Moodipy
Uses sentiment analysis to create a playlist on spotify that matches someone's mood and also predict songs to rise in popularity.
* Users are able to choose whether to create a playlist based on their spotify data, such as liked songs and top artists, or from their own public playlists.
* We used the newest songs of the week and current top 50 Global Songs on spotify to predict which new songs are most likely going to rise in popularity.

## Installation instructions

### Package name for PIP installation:
* pip install Moodipy==0.128
### Executable command:
* Moodipy
### Link to repository:
* https://github.com/dianas11xx/Moodify

### App Requirements
* In our current prototype, the user needs to have:
  *  A spotify premium account 
  *  Some liked songs/data in their library
  *  Public Playlists if they would like to try to create a playlist from one of their existing playlists
### If you get the Error: Could not load the Qt platform plugin :
  * qt.qpa.plugin: Could not load the Qt platform plugin "xcb" in "" even though it was found.
This application failed to start because no Qt platform plugin could be initialized. Reinstalling the application may fix this problem.
* Then run: 
  * sudo apt-get install libqt5x11extras5

### Required packages commands if the distribution is not found in PYPI: 
* screeninfo:
  * pip install screeninfo
* spotipy
  * pip install spotipy
* urllib3==1.26.6:
  * pip install urllib3 --upgrade
* requests>=2.25.0
  *  pip install requests --upgrade
* PyQt5:
  * pip3 install --user pyqt5
  * sudo apt-get install pyqt5-dev-tools
  * sudo apt-get install qttools5-dev-tools



