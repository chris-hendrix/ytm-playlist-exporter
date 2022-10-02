import os
import json
import glob
from pathlib import Path
import pandas as pd
from rapidfuzz import process
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
        files = get_files(self.settings['libraryDirectory'])
        for file in files:
            filename = Path(file).stem
            song_files.append({'file': file, 'filename': filename})
        return pd.DataFrame.from_dict(song_files)

    def get_playlist_songs(self):
        playlist_songs = []
        playlists = self.ytmusic.get_library_playlists()
        for playlist in playlists:
            playlist_id = playlist['playlistId']
            playlist_name = playlist['title']
            playlist_details = self.ytmusic.get_playlist(playlist_id, limit=500)
            for track in playlist_details['tracks']:
                artist = track['artists'][0]['name'] if len(track['artists']) > 0 else None
                title = track['title']
                album = track['album']['name'] if track['album'] else None
                filename = ' - '.join([artist or '', title or '', album or ''])
                playlist_songs.append({
                    'playlist': playlist_name,
                    'artist': artist,
                    'title': title,
                    'album': album,
                    'filename': filename
                })
        return pd.DataFrame.from_dict(playlist_songs)

    def get_playlist_song_files(self, score_cutoff=90):
        song_files = self.get_song_files()
        playlist_songs = self.get_playlist_songs()

        files = sorted(list(song_files['filename'].unique()))
        songs = sorted(list(playlist_songs['filename'].unique()))

        print(f'{len(files)} files and {len(songs)} unique songs')

        # first pass for exact matches
        exact_matches, exact_misses = [], []
        for song in songs:
            if song in files:
                exact_matches.append({'filename_song': song, 'filename_file': song})
                files.pop(files.index(song))
            else:
                exact_misses.append(song)
        print(f'{len(exact_matches)} exact matches with {len(exact_misses)} misses.')

        # second pass for fuzzy matches
        fuzzy_matches, fuzzy_misses = [], []
        for song in exact_misses:
            match = process.extractOne(song, files, score_cutoff=score_cutoff)
            if match:
                file = match[0]
                fuzzy_matches.append({'filename_song': song, 'filename_file': file})
                files.pop(files.index(file))
            else:
                fuzzy_misses.append(song)
        print(f'{len(fuzzy_matches)} fuzzy matches with {len(fuzzy_misses)} misses.')

        matches = pd.DataFrame.from_dict(exact_matches + fuzzy_matches)
        cols = playlist_songs.columns.difference(song_files.columns)
        playlist_song_files = pd.merge(playlist_songs, matches, left_on='filename', right_on='filename_song')
        playlist_song_files = pd.merge(playlist_song_files, song_files, left_on='filename_file', right_on='filename')
        return playlist_song_files[[*cols, 'file']]

    def export_playlists(self):
        def _replace(value):
            replacers = self.settings['fileReplacers']
            for f, r in replacers:
                value = value.replace(f, r)
            return value

        export_dir = self.settings['exportDirectory']
        playlist_song_files = self.get_playlist_song_files()
        playlist_song_files['filestr'] = playlist_song_files['file'].apply(lambda x: _replace(x))
        playlists = playlist_song_files['playlist'].unique()
        for playlist in playlists:
            filtered = list(playlist_song_files[playlist_song_files['playlist'] == playlist]['filestr'])
            export_path = os.path.join(export_dir, playlist + '.m3u')
            textfile = open(export_path, 'w')
            print(f'writing {playlist} ({len(filtered)} songs) to {export_path}')
            [textfile.write(f + '\n') for f in filtered]


if __name__ == "__main__":
    ytm = YtmExporter()
    # playlist_song_files = ytm.get_playlist_song_files()
    ytm.export_playlists()
