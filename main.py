import os
import sys
import subprocess
import requests
import json
import tempfile
import socket
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, TIT2, TPE1

def is_connected():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except OSError:
        return False

def embed_thumbnail(mp3_path, thumbnail_url, title=None, artist=None):
    audio = MP3(mp3_path, ID3=ID3)
    try:
        audio.add_tags()
    except Exception:
        pass

    try:
        img_data = requests.get(thumbnail_url).content
        audio.tags.add(APIC(
            encoding=3,
            mime='image/jpeg',
            type=3,
            desc='Cover',
            data=img_data
        ))
        if title:
            audio.tags.add(TIT2(encoding=3, text=title))
        if artist:
            audio.tags.add(TPE1(encoding=3, text=artist))
        audio.save()
        print("Embedded thumbnail and metadata into MP3.")
    except Exception as e:
        print(f"Thumbnail embedding failed: {e}")

def get_ytdlp_path():
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base_path, 'yt-dlp.exe')

def download_video_or_playlist(url, format='mp3', quality=None, folder_path="Downloads"):
    subfolder = "MP3" if format == 'mp3' else "MP4"
    folder = os.path.join(folder_path, subfolder)
    os.makedirs(folder, exist_ok=True)
    output_template = os.path.join(folder, "%(title)s.%(ext)s")

    ytdlp = get_ytdlp_path()
    if not os.path.exists(ytdlp):
        raise FileNotFoundError("yt-dlp.exe not found. Make sure it's bundled with your app.")

    if format == 'mp3':
        with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as tmp_json:
            json_path = tmp_json.name

        command = [
            ytdlp,
            "--print-json",
            "-x", "--audio-format", "mp3",
            "--audio-quality", quality,
            "-o", output_template,
            url
        ]

        result = subprocess.run(command, capture_output=True, text=True)

        try:
            data = json.loads(result.stdout.splitlines()[0])
            mp3_file = os.path.join(folder, data['title'] + ".mp3")
            thumbnail_url = data.get('thumbnail', '')
            title = data.get('title', None)
            artist = data.get('uploader', None)

            embed_thumbnail(mp3_file, thumbnail_url, title, artist)
            return mp3_file

        except Exception as e:
            print(f"Could not process metadata or thumbnail: {e}")
            return None

    else:
        command = [
            ytdlp,
            "--yes-playlist",
            "-f", f"bestvideo[height<={quality}][ext=mp4]+bestaudio[ext=m4a]/mp4/best",
            "-o", output_template,
            url
        ]
        subprocess.run(command)
        return None
