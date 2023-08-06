from setuptools import setup

setup(
    name="Moodipy",
    version="0.128",
    packages=["Moodipy"],
    url="https://github.com/dianas11xx/Moodify",
    author="Noteworthy",
    license = "GPL 3",
    package_data = {"Moodipy":["*.txt", "imgs/*.png", "imgs/*.jpeg", "*.csv", "*.pkl"]},
    long_description = "Uses sentiment analysis to create a playlist that matches someone's mood and also predict songs to rise in popularity.",
    description="Spotify Playlist Generator based on Mood",
    install_requires=['screeninfo==0.6.7', 'spotipy==2.18.0', 'requests>=2.25.0', 'PyQt5>=5.12','urllib3==1.26.6', 'PyQt5-sip>=4.19.19', 'pandas>=1.3.0', 'scikit-learn>=0.24.2', 'joblib==1.0.1'],
    entry_points={"console_scripts": ["Moodipy=Moodipy.main:main"]},
)
