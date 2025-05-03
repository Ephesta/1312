#Eph was here 

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import yt_dlp as ytdl
import threading

def select_download_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        download_folder.set(folder_selected)

def download_video():
    url = url_entry.get()
    quality = quality_combobox.get()
    folder = download_folder.get()

    if not url:
        messagebox.showwarning("Uyarı", "Lütfen bir URL girin.")
        return

    if not folder:
        messagebox.showwarning("Uyarı", "Lütfen bir indirme klasörü seçin.")
        return

    ydl_opts = {
        'outtmpl': f'{folder}/%(title)s.%(ext)s',
    }

    if quality:
        ydl_opts.update({
            'format': f'bestvideo[height={quality}]+bestaudio/best'
        })

    try:
        progress.start()  # İndirme başladığında barı başlat
        download_button.config(state='disabled')  # İndirme butonunu devre dışı bırak
        with ytdl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        progress.stop()  # İndirme tamamlandığında barı durdur
        messagebox.showinfo("Başarılı", "İndirme tamamlandı.")
    except Exception as e:
        progress.stop()  # Hata durumunda barı durdur
        messagebox.showerror("Hata", f"Video alınamadı:\n{e}")
    finally:
        download_button.config(state='normal')  # İndirme butonunu tekrar aktif hale getir

def start_download_thread():
    t = threading.Thread(target=download_video)
    t.start()

root = tk.Tk()
root.title("YouTube Video İndirici")
root.geometry("400x300")  # Başlangıç boyutunu ayarladık
root.configure(bg="#F0F0F0")  # Arka plan rengi


title_label = tk.Label(root, text="YouTube Video İndirici", font=("Helvetica", 14), bg="#F0F0F0")
title_label.pack(pady=10)


tk.Label(root, text="YouTube URL:", bg="#F0F0F0").pack(pady=5)
url_entry = tk.Entry(root, width=40)
url_entry.pack()


tk.Label(root, text="Çözünürlük:", bg="#F0F0F0").pack(pady=5)
quality_combobox = ttk.Combobox(root, values=["1080p", "720p", "480p", "360p", "240p", "144p"], state="readonly")
quality_combobox.current(1)  # Default olarak 720p seçili
quality_combobox.pack()

# İndirme Klasörü Seçimi ve İndir Butonu
download_folder = tk.StringVar()

folder_frame = tk.Frame(root, bg="#F0F0F0")
folder_frame.pack(pady=10)

folder_button = tk.Button(folder_frame, text="Klasör Seç", command=select_download_folder, bg="#4CAF50", fg="white")
folder_button.pack(side="left", padx=5)

download_button = tk.Button(folder_frame, text="İndir", command=start_download_thread, bg="#FF5722", fg="white")
download_button.pack(side="left", padx=5)

tk.Label(root, textvariable=download_folder, bg="#F0F0F0").pack()

progress = ttk.Progressbar(root, length=300, mode='indeterminate')
progress.pack(pady=10)
progress.place(x=50, y=200)  
progress.place_forget()  

root.mainloop()
