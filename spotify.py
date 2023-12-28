import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

client_id = os.getenv('SPOTIFY_CLIENT_ID')
client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
playlist_id = "1UBMrKsd5kUgiUxjfjFHUZ"
redirect_uri = 'http://localhost:8789'
scope = 'playlist-modify-public'
user_id = 'nightw0rk'
auth = SpotifyOAuth(client_id=client_id,
                    client_secret=client_secret,
                    redirect_uri=redirect_uri,
                    scope=scope
                )
sp = spotipy.Spotify(auth_manager=auth)


def search_song(query) -> str | None:
    try:
        results = sp.search(q=query, limit=1)
        return results['tracks']['items'][0]['id']
    except Exception: # noqa
        return None
def get_playlist_tracks():
    tracks = []
    results = sp.playlist_items(playlist_id)
    tracks.extend(results['items'])

    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])

    return tracks

def is_song_in_playlist(track_id):
    playlist_tracks = get_playlist_tracks()
    for item in playlist_tracks:
        if track_id == item['track']['id']:
            return True
    return False

def add_song_to_playlist(song_id: str):
    try:
        if is_song_in_playlist(song_id):
            print('Song already in playlist')
            return True
        sp.playlist_add_items(playlist_id, [song_id])
        return True
    except Exception: # noqa
        return False