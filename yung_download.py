import os
import re

import moviepy.editor as mp
from pytube import YouTube

download_path = "./download/"
f = open("toDownload.txt", "r")
lines = f.readlines()
videos_urls = [url.strip() for url in lines if "youtube" in url or "youtu.be" in url or "spotify" in url and url.startswith("https://")]
download_quality = lines[0].strip()
f.close()
file_list = []
all_quality = ["360", "720", "1080","1440","2160"]

def combine_audio(vidname, audname, outname, fps=60):
    import moviepy.editor as mpe
    my_clip = mp.VideoFileClip(vidname)
    audio_background = mp.AudioFileClip(audname)
    final_clip = my_clip.set_audio(audio_background)
    final_clip.write_videofile(outname, fps=fps, verbose=False)
    del my_clip.reader
    del my_clip
    del audio_background
    del final_clip.reader
    del final_clip

def download_mp3(url):
    yt = YouTube(url)
    qualities = yt.streams.filter(mime_type='video/mp4')
    sound_to_download = [x for x in qualities if "acodec" in str(x)]
    title = re.sub(r'\W+', ' ', sound_to_download[0].title)
    sound_to_download[0].download(download_path, f"{title}")
    video = mp.VideoFileClip(download_path+f"{title}.mp4", verbose=False)
    video.audio.write_audiofile(download_path+f"{title}.mp3", verbose=False)
    del video.reader
    del video
    os.remove(download_path+f"{title}.mp4")

def download_mp4(url):
    yt = YouTube(url)
    qualities = yt.streams.filter(mime_type='video/mp4')
    sound_to_download = [x for x in qualities if "acodec" in str(x)]
    video_to_download = [
        x for x in qualities if download_quality in str(x)]
    if len(video_to_download) == 0:
        video_to_download = [x for x in qualities if all_quality[all_quality.index(
            download_quality)-1] in str(x)]
    title = re.sub(r'\W+', ' ', sound_to_download[0].title)
    sound_to_download[0].download(download_path, f"{title}")
    video = mp.VideoFileClip(download_path+f"{title}.mp4", verbose=False)
    video.audio.write_audiofile(download_path+f"{title}.mp3", verbose=False)
    del video.reader
    del video
    os.remove(download_path+f"{title}.mp4")
    video_to_download[0].download(download_path, f"{title}")
    combine_audio(download_path+f"{title}.mp4", download_path +f"{title}.mp3", download_path+f"{title}temp.mp4") 
    os.remove(download_path+f"{title}.mp4")
    os.remove(download_path+f"{title}.mp3")
    os.rename(download_path+f"{title}temp.mp4", download_path+f"{title}.mp4")


if ("mp3" in download_quality):
    for url in videos_urls:
        download_mp3(url)

if (download_quality in all_quality):
    for url in videos_urls:
        download_mp4(url)
