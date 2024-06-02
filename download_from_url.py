import os, re, math
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, font
from tqdm.auto import tqdm
from pytube import YouTube, Playlist
from mutagen.mp4 import MP4

def download_playlist_from_url(PLAYLIST_URL):
  download_button.place_forget()
  
  # Create a button to break loop if necessary
  break_loop = tk.IntVar()
  break_loop.set(0)
  break_button = tk.Button(text="Interrupt download", command=lambda: break_loop.set(1))
  break_button.place(x=190, y=95, width=400)

  playlist = Playlist(PLAYLIST_URL)
  if(not playlist):
    messagebox.showerror("Error", "Couldn't retrieve playlist data, make sure it exists and it's not private")
    break_button.place_forget()
    download_button.place(x=190, y=95, width=400)
    return False
  playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")
  title = playlist.title
  whitelist = set('abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ')
  folder_name = dest_folder.get() + ''.join(filter(whitelist.__contains__, title)).replace(" ", "_")
  
  os.system('clear')
  print("\n--------------------------------------------------")
  print("Downloading: " + title + " to " + folder_name)
  print("--------------------------------------------------\n")
  
  total_playlist = len(playlist)
  current_downloaded = 0
 
  for url in tqdm(playlist):
    shoul_break = break_loop.get()
    if(shoul_break == 1):
      current_song.set("Download interrupted")
      messagebox.showinfo("Interrupt","Download interrupted, downloaded " + str(current_downloaded) + " songs")
      break

    retries = 0
    current_downloaded = current_downloaded + 1
    progress.set(math.ceil(current_downloaded * 100 / total_playlist))
    progress_text.set(str(progress.get()) + "%")
    window.update()
    while(retries < 3):
      try:
        video = YouTube(url)
        current_song.set("Downloading: " + video.title)
        window.update()
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
  os.system('clear')
  last_progress = progress.get()
  if(last_progress >= 100):
    current_song.set("Download complete")
    messagebox.showinfo("Success","Successfully downloaded " + str(current_downloaded) + " songs")
  progress.set(100)
  progress_text.set("")
  break_button.place_forget()
  download_button.place(x=190, y=95, width=400)
  window.update()
  
def destination_folder():
  selected_folder = filedialog.askdirectory()
  if(not selected_folder):
    selected_folder = "./"
  else:
    selected_folder = str(selected_folder + "/").replace("//", "/")
  dest_folder.set(selected_folder)
  window.update()

window = tk.Tk()        
window.title("YouTube Playlist Download")
window.geometry("800x170")

# Playlist URL Field
playlist_url_label = tk.Label(text="Paste playlist URL:")
playlist_url_label.place(x=10, y=5)

playlist_url = tk.StringVar()
playlist_url.set("https://www.youtube.com/playlist?list=PLqDLcuYrEYqmL29OPnHZ26XRYT6A2FzSK")
playlist_url_entry = tk.Entry(window, textvariable=playlist_url)
playlist_url_entry.place(x=10, y=25, width=780, height=25)

# Dest folder field
dest_folder_label = tk.Label(text="Select destination folder:")
dest_folder_label.place(x=10, y=45)

dest_folder = tk.StringVar()
dest_folder.set("./")
dest_folder_entry = tk.Entry(window, textvariable=dest_folder)
dest_folder_entry.place(x=10, y=65, width=690, height=25)

## Dest folder button
dest_folder_button = tk.Button(text="Select folder", font = tk.font.Font(size = 8), command=lambda: destination_folder())
dest_folder_button.place(x=710, y=65, width=80, height=25)

## Download button
download_button = tk.Button(text="Download playlist", command=lambda: download_playlist_from_url(playlist_url.get()))
download_button.place(x=190, y=95, width=400, height=25)

# Current downloading
current_song = tk.StringVar()
current_song.set("")
current_song_label = tk.Label(textvariable=current_song)
current_song_label.place(x=10, y=125)

# Progress Bar
progress = tk.IntVar()
progress.set(0)
progress_text = tk.StringVar()
progress_text.set("")
progressbar_label = tk.Label(textvariable=progress_text)
progressbar_label.place(x=765, y=125)
progressbar = ttk.Progressbar(variable=progress)
progressbar.place(x=10, y=145, width=780)

# window.directory = filedialog.askdirectory()

window.mainloop()
