
import os
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from pytube import YouTube
import tkinter.filedialog as filedialog

ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
DOWNLOAD_PATH = os.path.join(ROOT_PATH, "youtube")

class StatusBar():
    def init(self, window, msg):
        self.window = window        
        self.var = StringVar()
        self.entry = Entry(window, state='readonly', readonlybackground="#dfdfdf", fg='black')
        self.entry.grid(row=3, column=0, columnspan=2, sticky="we")
        self.entry.config(textvariable=self.var, relief='flat')
        self.set(msg)

    def get(self):
        return self.var.get()

    def set(self, msg):
        self.var.set(msg)
        self.entry.update()


def create_image_dir(dir):
    try:
        if not(os.path.isdir(dir)):
            os.makedirs(os.path.join(dir))
            print("DIR: ", dir)
    except Exception as e:
            print("Failed to create directory:", e)
            exit()

statusBar = StatusBar()

def download_youtube(url, path):
    yt = YouTube(url)
    parent_dir = path
    statusBar.set("Downloading ...")
    yt.streams.filter(subtype='mp4').first().download(parent_dir)
    statusBar.set("DONE: " + str(path))

def main():
    window = Tk()
    window.title("Youtube Download")
    window.resizable(width=True, height=False)

    input_url = StringVar()
    input_dir = StringVar()
    input_dir.set(DOWNLOAD_PATH)

    def btn_download():
        url = input_url.get()
        dir = input_dir.get()
        print('URL', url)
        print('DIR', dir)
        create_image_dir(dir)
        download_youtube(url, dir)

    def btn_saveto():
        dir = filedialog.askdirectory(parent = window, initialdir = ROOT_PATH, title='Download a directory')
        if dir:
            input_dir.set(dir)

    ttk.Label(window, text = "Youtube URL\t").grid(row = 0, column = 0, sticky=W)
    ttk.Button(window, text="SAVE To\t", command=btn_saveto).grid(row = 1, column = 0, sticky=W)
    ttk.Entry(window, textvariable = input_url).grid(row = 0, column = 1, padx = 5, pady = 5, ipadx=200)    
    ttk.Entry(window, textvariable = input_dir).grid(row = 1, column = 1, padx = 5, pady = 5, ipadx=200)
    ttk.Button(window, text="Download", command=btn_download).grid(row = 2, column = 1, padx = 10, pady = 10)  
    statusBar.init(window, "Ready")    

    window.mainloop()

if __name__ == "__main__":
	main()