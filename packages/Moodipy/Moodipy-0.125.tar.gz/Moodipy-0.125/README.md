# Moodipy
Uses sentiment analysis to create a playlist on spotify that matches someone's mood and also predict songs to rise in popularity.
* Users are able to choose whether to create a playlist based on their spotify data, such as liked songs and top artists, or from their own public playlists.
* We used the newest songs of the week and current top 50 Global Songs on spotify to predict which new songs are most likely going to rise in popularity.

## Installation instructions

### Package name for PIP installation:
* pip install Moodipy==0.124
### Executable command:
* Moodipy
### Link to repository:
* https://github.com/dianas11xx/Moodify

### App Requirements
* In our current prototype, the user needs to have a spotify premium account and have some liked songs/data in their library. 

### Required packages commands if the distribution is not found in PYPI: 
* screeninfo:
  * pip install screeninfo
* spotipy
  * pip install spotipy
* urllib3==1.26.6:
  * pip install urllib3 --upgrade
* requests>=2.25.0
  *  pip install requests --upgrade
* nltk:
  * pip install nltk
  * python3 -m nltk.downloader punkt
  * python3 -m nltk.downloader stopwords
  * python3 -m nltk.downloader averaged_perceptron_tagger
  * python3 -m nltk.downloader wordnet
* PyQt5:
  * pip3 install --user pyqt5
  * sudo apt-get install pyqt5-dev-tools
  * sudo apt-get install qttools5-dev-tools



