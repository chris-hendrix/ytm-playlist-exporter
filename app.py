import os
import json
import glob
from pathlib import Path
import pandas as pd
import difflib
from ytmusicapi import YTMusic


def get_files(dir, latest=False):
    files = glob.glob(dir + '/*', recursive=True)
    files = [os.path.abspath(f) for f in files]
    return files


class YtmExporter:
    def __init__(self):
        self.settings = json.load(open('settings.json'))
        self.ytmusic = YTMusic('headers_auth.json', self.settings['id'])

    def get_song_files(self):
        song_files = []
        files = get_files(self.settings['libraryPath'])
        for file in files:
            filename = Path(file).stem
            song_files.append({'file': file, 'filename': filename})
        return pd.DataFrame.from_dict(song_files)

    def get_playlist_songs(self):
        playlist_songs = []
        playlists = self.ytmusic.get_library_playlists()
        for playlist in playlists[0:1]:
            playlist_id = playlist['playlistId']
            playlist_name = playlist['title']
            playlist_details = self.ytmusic.get_playlist(playlist_id)
            for track in playlist_details['tracks']:
                artist = track['artists'][0]['name']
                title = track['title']
                album = track['album']['name']
                filename = ' - '.join([artist, title, album])
                playlist_songs.append({
                    'playlist': playlist_name,
                    'artist': artist,
                    'title': title,
                    'album': album,
                    'filename': filename
                })
        return pd.DataFrame.from_dict(playlist_songs)

    def get_playlist_song_files(self):
        def _get_close_match(text, column):
            matches = difflib.get_close_matches(text, column)
            return matches[0] if len(matches) > 0 else None

        song_files = self.get_song_files()
        playlist_songs = self.get_playlist_songs()
        playlist_songs_col = pd.DataFrame(playlist_songs.groupby(['filename']), columns=['filename', 'agg'])['filename']
        song_files['filename_match'] = song_files['filename'].map(lambda x: _get_close_match(x, playlist_songs_col))
        return playlist_songs


if __name__ == "__main__":
    ytm = YtmExporter()
    playlist_song_files = ytm.get_playlist_song_files()
    print(playlist_song_files.head())
