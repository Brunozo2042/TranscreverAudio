from __future__ import unicode_literals
import yt_dlp
import ffmpeg
import sys
import os

# Garante que a pasta "audios" existe
output_dir = "audios"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Define o caminho de saída na pasta "audios"
ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'wav',
    }],
}

def download_from_url(url):
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    args = sys.argv[1:]
    if len(args) > 1:
        print("Too many arguments.")
        print("Usage: python youtubetowav.py <optional link>")
        print("If a link is given it will automatically convert it to .wav. Otherwise a prompt will be shown")
        exit()
    if len(args) == 0:
        url = input("Enter Youtube URL: ")
        download_from_url(url)
    else:
        download_from_url(args[0])

# Transcrever o audio
# os.system("python audiototext.py")