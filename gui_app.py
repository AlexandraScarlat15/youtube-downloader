import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from main import is_connected, download_video_or_playlist
import os

# ------------------- Functions -------------------
def start_download():
    url = url_entry.get()
    format_choice = format_var.get()
    quality_choice = quality_var.get()
    folder = output_folder.get()

    if not url.strip():
        messagebox.showerror("Error", "Please paste a YouTube link.")
        return

    if not is_connected():
        messagebox.showerror("No Internet", "Please connect to the internet.")
        return

    status_var.set("Downloading... Please wait.")
    app.update()

    try:
        mp3_path = download_video_or_playlist(url, format_choice, quality_choice, folder)
        status_var.set("Download complete!")
    except Exception as e:
        status_var.set("Error during download")
        messagebox.showerror("Error", str(e))

def update_quality_options(event=None):
    fmt = format_var.get()
    if fmt == "mp3":
        quality_dropdown["values"] = ["128k", "192k", "256k", "320k"]
        quality_var.set("192k")
    else:
        quality_dropdown["values"] = ["360", "480", "720", "1080", "best"]
        quality_var.set("best")

def choose_folder():
    selected = filedialog.askdirectory()
    if selected:
        output_folder.set(selected)

# ------------------- GUI SETUP -------------------

app = tk.Tk()
app.title("YouTube Downloader")
app.geometry("420x420")
app.configure(bg="#1f1f2e")
bg_color = "#1f1f2e"
button_color = "#00bfff"
font = ("Segoe UI", 10)

style = ttk.Style()
style.theme_use('default')
style.configure("TLabel", background=bg_color, foreground="white", font=font)
style.configure("TButton", padding=6, font=("Segoe UI", 10, "bold"))
style.configure("TEntry", padding=5)
style.configure("TCombobox", padding=5)

# URL Entry
url_label = tk.Label(app, text="YouTube Link:", bg=bg_color, fg="white", font=font)
url_label.pack(pady=(10, 0))
url_entry = tk.Entry(app, width=50, font=font)
url_entry.pack(pady=5)
try:
    clip = app.clipboard_get()
    if any(site in clip for site in ["youtube.com", "youtu.be"]):
        url_entry.insert(0, clip)
except:
    pass

# Folder
output_folder = tk.StringVar()
output_folder.set("Downloads")
tk.Label(app, text="Save to Folder:", bg=bg_color, fg="white", font=font).pack()
folder_frame = tk.Frame(app, bg=bg_color)
folder_frame.pack(pady=5)
folder_entry = tk.Entry(folder_frame, textvariable=output_folder, width=38, font=font)
folder_entry.pack(side=tk.LEFT)
tk.Button(folder_frame, text="Browse", command=choose_folder, bg=button_color, fg="white", font=font).pack(side=tk.LEFT, padx=5)

# Format Toggle
tk.Label(app, text="Choose Format:", bg=bg_color, fg="white", font=font).pack()
format_var = tk.StringVar(value="mp3")
format_dropdown = ttk.Combobox(app, textvariable=format_var, values=["mp3", "mp4"], state="readonly", font=font)
format_dropdown.pack(pady=5)
format_dropdown.bind("<<ComboboxSelected>>", update_quality_options)

# Quality
tk.Label(app, text="Quality:", bg=bg_color, fg="white", font=font).pack()
quality_var = tk.StringVar()
quality_dropdown = ttk.Combobox(app, textvariable=quality_var, state="readonly", font=font)
quality_dropdown.pack(pady=5)
update_quality_options()

# Download button
tk.Button(app, text="Convert", command=start_download, bg=button_color, fg="white", font=("Segoe UI", 12, "bold"), padx=10, pady=5).pack(pady=20)

# Status label
status_var = tk.StringVar()
status_label = tk.Label(app, textvariable=status_var, bg=bg_color, fg="lightgreen", font=("Segoe UI", 9, "italic"))
status_label.pack()

app.mainloop()
