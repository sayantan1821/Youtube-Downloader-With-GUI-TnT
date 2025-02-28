# libraraies

from pytube import *
import os
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import *
from tkinter.messagebox import *
from threading import *

file_size = 0
resolution = "1080p"

OPTIONS = [
    "1080p",
    "720p",
    "480p",
    "360p",
    "240p",
    "144p",
    "Only Audio (mp3)"
]

def progress_function(stream=None, chunk=None, remaining=None):
    file_downloaded = (file_size-remaining)
    per = round((file_downloaded/file_size)*100, 1)
    print(str(per)+'%')
    progress['value'] = per
    main.update_idletasks()


# function start download to start the download of files
def startDownload():
    global file_size
    try:
        URL = urlField.get()
        regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
        pat = re.compile(regex)
         if not re.fullmatch(pat, URL):
            showinfo("Enter valid URL", 'Enter a valid URL')
        else:
            dBtn.config(text="Please wait...")
            dBtn.config(state=DISABLED)
            path_save = askdirectory()
            if path_save is None:
            return
            ob = YouTube(URL, on_progress_callback=progress_function)
            strm = ob.streams[0]
            x = ob.description.split("|")
            file_size = strm.filesize
            dfile_size = file_size
            dfile_size /= 1000000
            dfile_size = round(dfile_size, 2)
            label.config(text="Size: " + str(dfile_size) + " MB")
            label.pack(side=TOP, pady=10)
            desc.config(
                text=ob.title
                + "\n\n"
                + "Label: "
                + ob.author
                + "\n\n"
                + "length: "
                + str(round(ob.length / 60, 1))
                + " mins\n\n"
                "Views: " + str(round(ob.views / 1000000, 2)) + "M"
            )
            desc.pack(side=TOP, pady=10)
            strm.download(path_save, strm.title)
            dBtn.config(state=NORMAL)
            showinfo("Download Finished", "Downloaded Successfully")
            urlField.delete(0, END)
            label.pack_forget()
            desc.pack_forget()
            progress['value'] = 0
            dBtn.config(text="Start Download")

    except Exception as e:
        print(e)
        print("Error!!")
        showinfo("ERROR", 'OOPS! AN ERROR OCCURED')
        dBtn.config(state=NORMAL)
        urlField.delete(0, END)
        label.pack_forget()
        desc.pack_forget()
        myCombo.current(0)
        progress['value'] = 0
        dBtn.config(text='Start Download')


def startDownloadthread():
    thread = Thread(target=startDownload)
    thread.start()


# main functions
main = Tk()

progress = ttk.Progressbar(main, orient = HORIZONTAL, length = 400, mode = 'determinate')

main.title("My YouTube Downloader")
main.config(bg="#3498DB")

main.iconbitmap("youtube-ios-app.ico")

main.geometry("500x600")

file = PhotoImage(file="photo.png")
headingIcon = Label(main, image=file)
headingIcon.pack(side=TOP)

urlField = Entry(main, font=("Times New Roman", 18), justify=CENTER)
urlField.pack(side=TOP, fill=X, padx=10, pady=15)

progress.pack(padx=10, pady=15)

dBtn = Button(
    main,
    text="Start Download",
    font=("Times New Roman", 18),
    relief="ridge",
    activeforeground="red",
    command=startDownloadthread,
)
dBtn.pack(side=TOP)
label = Label(main, text="")
desc = Label(main, text="")
main.mainloop()
