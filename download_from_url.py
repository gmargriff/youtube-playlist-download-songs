import sys, re, os
from tqdm.auto import tqdm
from pytube import YouTube, Playlist
from mutagen.mp4 import MP4

if len(sys.argv) > 1:
    PLAYLIST_URL = sys.argv[1]
else:
    print("Missing playlist URL")
    quit()

playlist = Playlist(PLAYLIST_URL)
#playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")
title = playlist.title
whitelist = set('abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ')
folder_name = "./" + ''.join(filter(whitelist.__contains__, title)).replace(" ", "_")

os.system('clear')
print("\n--------------------------------------------------")
print("Downloading: " + title)
print("--------------------------------------------------\n")
  
for url in tqdm(playlist):
  retries = 0
  while(retries < 3):
    try:
      video = YouTube(url)
      if(not os.path.isfile(folder_name + "/" + video.title + ".mp4")):
        audio = video.streams.filter(only_audio=True)[0]
        downloaded = audio.download(output_path=folder_name)
        audiofile = MP4(downloaded)
        audiofile["title"] = video.title
        audiofile["artist"] = video.author
        audiofile.pprint()
        audiofile.save()
      retries = 3
    except:
      retries = retries + 1
      if(retries >= 3):
        print("Error while downloading: " + video.title)
