# YTM Playlist Exporter
Downloads YTM playlists using [ytmusicapi](https://github.com/sigma67/ytmusicapi) and creates local m3u files based on a local folder of music, using fuzzy matching to match the file names.

### Install
Setup venv
```
virtualenv -p $(which python3) venv
```
Activate venv and install packages
```
source venv/bin/activate
pip install --upgrade pip
pip install flake8
pip install -e .
pip install ytmusicapi
pip install pandas
pip install rapidfuzz
```
### Setup
1. Create `headers_raw.txt` file with the pasted headers per the instructions of ytmusicapi.
1. Create a `settings.json` file
```
{
  "id": <google user id, see ytmusicapi>,
  "libraryDirectory": <local music directory>,
  "exportDirectory": <playlist export directory>,
  "fileReplacers": [
    [<find>, <replacer>],
    [<find>, <replacer>]
  ]
}
```
### Run
```
python app.py
```