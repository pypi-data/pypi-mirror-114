import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
import requests.exceptions

# Class for the Spotify Client
class Spotify(object):
    # Client Variables
    _client_id = None
    _client_secret = None
    _redirect_uri = None
    _spotify_client = None
    _cache_path = None

    # Constructor
    def __init__(self, client_id=None, client_secret=None, redirect_uri=None, cache_path=None):
        if client_id == None or client_secret == None:
            raise Exception("You must set client_id and client_secret")

        if redirect_uri == None:
            raise Exception("You must set a redirect_uri")

        self._client_id = client_id
        self._client_secret = client_secret
        self._redirect_uri = redirect_uri
        self._cache_path = cache_path
        cache_handle = spotipy.cache_handler.CacheFileHandler(cache_path=self._cache_path)
        self._spotify_client = spotipy.Spotify(
            client_credentials_manager=SpotifyClientCredentials(client_id, client_secret, cache_handler=cache_handle))

        if not self._spotify_client:
            raise Exception("An error occurred on the client side")


# Class for the User
class User(Spotify):
    # User Variables
    _user_token = None
    _user_client = None
    _user_id = None


    # Constructor
    def __init__(self, user_id=None, scope=None, client=None):
        self._user_id = user_id
        self._user_token = util.prompt_for_user_token(user_id, scope, client._client_id, client._client_secret,
                                                      client._redirect_uri, client._cache_path)
        self._user_client = spotipy.Spotify(auth=self._user_token)

        if not self._user_client:
            raise Exception("An error occurred granting access")

    # Returns a List of the Users Liked Songs
    def get_user_saved_tracks(self):
        i, items, results = 0, ['1'], []
        while (len(items) > 0):
            try:
                items = self._user_client.current_user_saved_tracks(50, 50 * i)['items']
            except(spotipy.exceptions.SpotifyException, requests.exceptions.HTTPError,spotipy.oauth2.SpotifyOauthError):
                return results
            if (len(items) != 0):
                for item in items:
                    results.append(item['track'])
            i += 1
            if i > 10:  # FOR TESTING PURPOSES, 100 songs only
                break
        return results

    # Returns a List of Users Top Tracks
    def get_user_top_tracks(self):
        i, items, results = 0, ['1'], []
        while (len(items) > 0):
            try:
                items = self._user_client.current_user_top_tracks(50, 50 * i)['items']
            except(spotipy.exceptions.SpotifyException, requests.exceptions.HTTPError,spotipy.oauth2.SpotifyOauthError):
                return results

            if (len(items) != 0):
                for item in items:
                    results.append(item)

            i += 1

            if i > 10:
                break

        return results

    def get_user_top_artists_tracks(self):
        i, items, results = 0, ['1'], []
        while (len(items) > 0):
            try:
                items = self._user_client.current_user_top_artists(50, 50 * i)['items']
            except(spotipy.exceptions.SpotifyException, requests.exceptions.HTTPError, spotipy.oauth2.SpotifyOauthError):
                return results
            if (len(items) != 0):
                for item in items:
                    top = []
                    try:
                        top = self._user_client.artist_top_tracks(item['uri'])
                    except(spotipy.exceptions.SpotifyException, requests.exceptions.HTTPError,
                           spotipy.oauth2.SpotifyOauthError):
                        return results
                    results.extend(top['tracks'])
            i += 1
            if i > 10:  # FOR TESTING PURPOSES, 100 songs only
                break
        return results


    # Returns a List of the Users Songs Matching Emotion
    def get_user_emotion_tracks(self, client=None, user_tracks=None, base_emotion=None, second_emotion=""):
        emotion_tracks = []
        if base_emotion == "sadness" or base_emotion == "awful" or second_emotion == "sadness" or second_emotion == "awful":
            for track in user_tracks:
                af = client._spotify_client.audio_features(track['uri'])[0]
                num_hits = 0
                if af is not None:
                    if af['valence'] < 0.5:
                        num_hits += 1
                    if af['energy'] < 0.5:
                        num_hits += 1
                    if af['instrumentalness'] > 0.5:
                        num_hits += 1
                    if af['acousticness'] > 0.5:
                        num_hits += 1
                    if af['tempo'] < 120:
                        num_hits += 1
                    if num_hits > 3:
                        emotion_tracks.append(track)

        elif base_emotion == "bad" or base_emotion == "anger":
            for track in user_tracks:
                af = client._spotify_client.audio_features(track['id'])[0]
                num_hits = 0
                if af is not None:
                    if af['loudness'] > 0.5:
                        num_hits += 1
                    if af['energy'] > 0.5:
                        num_hits += 1
                    if af['tempo'] > 120:
                        num_hits += 1
                    if af['speechiness'] > 0.5:
                        num_hits += 1
                    if num_hits > 3:
                        emotion_tracks.append(track)

        elif base_emotion == "okay" or base_emotion == "fear":
            for track in user_tracks:
                af = client._spotify_client.audio_features(track['id'])[0]
                num_hits = 0
                if af is not None:
                    if af['danceability'] < 0.5:
                        num_hits += 1
                    if af['instrumentalness'] > 0.5:
                        num_hits += 1
                    if af['loudness'] > 0.5:
                        num_hits += 1
                    if af['valence'] < 0.5:
                        num_hits += 1
                    if af['energy'] <= 0.5:
                        num_hits += 1
                    if num_hits > 3:
                        emotion_tracks.append(track)

        elif base_emotion == "happy" or base_emotion == "joy":
            for track in user_tracks:
                af = client._spotify_client.audio_features(track['id'])[0]
                num_hits = 0
                if af is not None:
                    if af['valence'] > 0.5:
                        num_hits += 1
                    if af['danceability'] > 0.5:
                        num_hits += 1
                    if af['energy'] > 0.5:
                        num_hits += 1
                    if af['tempo'] > 100:
                        num_hits += 1
                    if af['loudness'] > 0.5:
                        num_hits += 1
                    if num_hits > 3:
                        emotion_tracks.append(track)

        elif base_emotion == "excited" or base_emotion == "surprise":
            for track in user_tracks:
                af = client._spotify_client.audio_features(track['id'])[0]
                num_hits = 0
                if af is not None:
                    if af['energy'] > 0.5:
                        num_hits += 1
                    if af['loudness'] > 0.5:
                        num_hits += 1
                    if af['tempo'] > 120:
                        num_hits += 1
                    if af['danceability'] > 0.5:
                        num_hits += 1
                    if num_hits > 3:
                        emotion_tracks.append(track)

        elif base_emotion == "love":
            for track in user_tracks:
                af = client._spotify_client.audio_features(track['id'])[0]
                num_hits = 0
                if af is not None:
                    if af['valence'] > 0.5:
                        num_hits += 1
                    if af['tempo'] < 120:
                        num_hits += 1
                    if af['instrumentalness'] < 0.5:
                        num_hits += 1
                    if af['mode'] == 0:
                        num_hits += 1
                    if num_hits > 3:
                        emotion_tracks.append(track)

        return emotion_tracks

    def get_user_playlists(self):
        i, items, results = 0, ['1'], []
        while (len(items) > 0):
            try:
                items = self._user_client.current_user_playlists(50, 50 * i)['items']
            except(spotipy.exceptions.SpotifyException, requests.exceptions.HTTPError, spotipy.oauth2.SpotifyOauthError):
                return results
            if (len(items) > 0):
                for item in items:
                    results.append(item)

            i += 1

        return results

    def get_user_playlist_tracks(self, playlist_id=None):
        i, items, results = 0, ['1'], []
        while (len(items) > 0):
            try:
                items = self._user_client.playlist_tracks(playlist_id, limit=50, offset=50 * i)['items']
            except(spotipy.exceptions.SpotifyException, requests.exceptions.HTTPError, spotipy.oauth2.SpotifyOauthError):
                return results
            if (len(items) != 0):
                for item in items:
                    results.append(item['track'])
                i += 1
                if i > 10:
                    break
            return results


    # Creates a New Playlist for the User
    def create_playlist(self, playlist_name=None, public=True, collaborative=False, description=""):
        if playlist_name == None:
            raise Exception("You must enter a playlist name")

        return (self._user_client.user_playlist_create(self._user_id, name=playlist_name, public=public,
                                                       collaborative=collaborative, description=description))['id']
    # Adds Tracks to a User's Playlist
    def add_to_playlist(self, playlist_id=None, playlist_tracks=None):
        track_ids = []
        for track in playlist_tracks:
            track_ids.append(track['id'])
        if len(playlist_tracks) < 100:
            self._user_client.user_playlist_add_tracks(self._user_id, playlist_id=playlist_id, tracks=track_ids)
        else:
            for i in range(0, len(track_ids), 50):
                hundred_tracks = track_ids[i:i + 50]
                self._user_client.user_playlist_add_tracks(self._user_id, playlist_id=playlist_id,
                                                           tracks=hundred_tracks)

"""
    /* USER INPUT PARAMETERS */
    Values from 0 - 1
    float acousticness;                   //Metric of the track being acoustic
    float danceability;                   //Metric of the track being danceable
    float energy;                         //Metric of the energy of the track
    float instrumentalness;               //Metric of the track being instrumental
    float liveness;                       //Metric of the track sounding as a live performance
    float speechiness;                    //Metric of the track containing human voice
    float valence;                        //Metric of the positiveness of the track
    float tempo;                          //The tempo of the track in BPM as its reciprocal
    float loudness;                       //Metric of the loudness of the track
    bool mode;                            //Whether the track is major or minor
    float popularity;                     //Metric of the popularity of the track
"""
