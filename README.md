# YTM Playlist Exporter

Exports YouTube Music playlists to .m3u files using fuzzy matching with your local music library.

## Features

- Exports YouTube Music playlists to .m3u format
- Fuzzy matching between playlist songs and local files
- Skips podcast playlists automatically
- Browser-based authentication (no API keys)

## Setup

**Install dependencies:**
```bash
pip install -r requirements.txt
```

**Authentication:**
1. Open YouTube Music in browser → Developer Tools (`F12`) → Network tab
2. Navigate in YouTube Music, find a POST request to `/browse` 
3. Copy request headers, then run:
   ```bash
   ytmusicapi browser
   ```
4. Paste headers and press `Ctrl+D`

**Configuration:**
```bash
cp settings.json.example settings.json
```
Edit paths in `settings.json`:
```json
{
  "libraryDirectory": "/path/to/your/music/library",
  "exportDirectory": "/path/to/export/playlists",
  "fileReplacers": [["/music/", "C:\\Music\\"], ["/", "\\"]]
}
```

## Usage

```bash
python app.py
```

Creates .m3u playlist files in your export directory by matching playlist songs with local files.

## Troubleshooting

- **Auth issues**: Ensure headers include `cookie` and `x-goog-authuser`
- **No matches**: Check `libraryDirectory` path and file naming
- **Path issues**: Use absolute paths, configure `fileReplacers` for your music player