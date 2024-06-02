import os, math
import tkinter as tk
from tkinter import ttk
from tqdm.auto import tqdm
from pytube import YouTube, Playlist
from mutagen.mp4 import MP4

def download_playlist_from_url(PLAYLIST_URL):
  download_button.pack_forget()
  playlist = Playlist(PLAYLIST_URL)
  title = playlist.title
  whitelist = set('abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ')
  folder_name = "./" + ''.join(filter(whitelist.__contains__, title)).replace(" ", "_")
  
  os.system('clear')
  print("\n--------------------------------------------------")
  print("Downloading: " + title)
  print("--------------------------------------------------\n")
  
  total_playlist = len(playlist)
  current_downloaded = 0
  
  for url in tqdm(playlist):
    retries = 0
    current_downloaded = current_downloaded + 1
    progress.set(math.ceil(current_downloaded * 100 / total_playlist))
    progress_text.set(str(progress.get()) + "%")
    window.update()
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


window = tk.Tk()        
window.title("YouTube Playlist Download")
window.geometry("800x110")

# Playlist URL Field
playlist_url_label = tk.Label(text="Paste playlist URL:")
playlist_url_label.pack()

playlist_url = tk.StringVar()
playlist_url.set("https://www.youtube.com/playlist?list=PLqDLcuYrEYqmL29OPnHZ26XRYT6A2FzSK")
playlist_url_entry = tk.Entry(window, width=80, textvariable=playlist_url)
playlist_url_entry.pack()

download_button = tk.Button(text="Download Playlist", command=lambda: download_playlist_from_url(playlist_url.get()))
download_button.pack()

# Progress Bar
progress = tk.IntVar()
progress.set(0)
progress_text = tk.StringVar()
progress_text.set(str(progress.get()) + "%")
progressbar_label = tk.Label(textvariable=progress_text)
progressbar_label.place(x=765, y=70)
progressbar = ttk.Progressbar(variable=progress)
progressbar.place(x=10, y=90, width=780)

window.mainloop()