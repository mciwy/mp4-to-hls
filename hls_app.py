import os
import json
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import urllib.request
import webbrowser

APP_VERSION = "1.0.1"
VERSION_URL = "https://raw.githubusercontent.com/mciwy/mp4-to-hls/main/version.json"
CONFIG_FILE = "config.json"

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_config(data):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def check_for_update():
    try:
        with urllib.request.urlopen(VERSION_URL) as response:
            data = json.loads(response.read().decode())
            latest_version = data["version"]
            changelog = data.get("changelog", "")
            download_url = data["download_url"]

            if latest_version != APP_VERSION:
                answer = messagebox.askyesno(
                    "Доступно обновление",
                    f"""Новая версия: {latest_version}

Изменения:
{changelog}

Скачать?"""
                )
                if answer:
                    webbrowser.open(download_url)
    except Exception as e:
        print("Ошибка проверки обновлений:", e)

def generate_hls(input_file, output_dir, bitrates, log_file, update_progress):
    renditions = [
        {'name': '480p', 'resolution': '854x480', 'bitrate': bitrates['480p']},
        {'name': '720p', 'resolution': '1280x720', 'bitrate': bitrates['720p']},
        {'name': '1080p', 'resolution': '1920x1080', 'bitrate': bitrates['1080p']},
    ]

    master_playlist = "#EXTM3U\n#EXT-X-VERSION:3\n"

    with open(log_file, "w", encoding="utf-8") as log:
        for i, r in enumerate(renditions):
            output_path = os.path.join(output_dir, r['name'])
            os.makedirs(output_path, exist_ok=True)

            segment_path = os.path.join(output_path, "segment_%03d.ts")
            m3u8_path = os.path.join(output_path, "index.m3u8")

            cmd = [
                "ffmpeg", "-y",
                "-i", input_file,
                "-vf", f"scale={r['resolution']}",
                "-c:a", "aac", "-ar", "48000", "-c:v", "h264",
                "-profile:v", "main", "-crf", "20", "-sc_threshold", "0",
                "-g", "48", "-keyint_min", "48",
                "-b:v", r['bitrate'], "-maxrate", r['bitrate'], "-bufsize", "1200k",
                "-hls_time", "6", "-hls_playlist_type", "vod",
                "-hls_segment_filename", segment_path,
                m3u8_path
            ]

            try:
                process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
                log.write(f"=== {r['name']} ===\n{process.stdout}\n")
                if process.returncode != 0:
                    raise RuntimeError(f"FFmpeg завершился с ошибкой: {process.returncode}")
            except Exception as e:
                log.write(f"Ошибка в {r['name']}: {e}\n")
                raise

            bandwidth = int(r['bitrate'].replace('k', '')) * 1000
            master_playlist += (
                f"#EXT-X-STREAM-INF:BANDWIDTH={bandwidth},RESOLUTION={r['resolution']}\n"
                f"{r['name']}/index.m3u8\n"
            )

            update_progress((i + 1) * 30)

        master_path = os.path.join(output_dir, "master.m3u8")
        with open(master_path, "w", encoding="utf-8") as f:
            f.write(master_playlist)

        update_progress(100)

def run_conversion():
    input_file = input_path.get()
    output_folder = output_path.get()
    bitrates = {
        "480p": bitrate_480.get() + "k",
        "720p": bitrate_720.get() + "k",
        "1080p": bitrate_1080.get() + "k",
    }

    if not os.path.isfile(input_file):
        messagebox.showerror("Ошибка", f"Файл не найден: {input_file}")
        return

    if not os.path.isdir(output_folder):
        messagebox.showerror("Ошибка", f"Папка не найдена: {output_folder}")
        return

    save_config({
        "input": input_file,
        "output": output_folder,
        "bitrates": {
            "480p": bitrate_480.get(),
            "720p": bitrate_720.get(),
            "1080p": bitrate_1080.get()
        }
    })

    log_file = os.path.join(output_folder, "conversion_log.txt")
    status_label.config(text="⏳ Конвертация... подождите.", fg="blue")
    progress_var.set(0)
    root.update()

    try:
        generate_hls(input_file, output_folder, bitrates, log_file, lambda p: progress_var.set(p))
        status_label.config(text="✅ Готово! Потоки созданы.", fg="green")
    except Exception as e:
        status_label.config(text="❌ Ошибка при конвертации.", fg="red")
        messagebox.showerror("FFmpeg Ошибка", str(e))

def browse_input():
    filename = filedialog.askopenfilename(filetypes=[("MP4 files", "*.mp4")])
    if filename:
        input_path.set(filename)

def browse_output():
    folder = filedialog.askdirectory()
    if folder:
        output_path.set(folder)

# === GUI ===
root = tk.Tk()
root.title(f"MP4 → HLS Конвертер v{APP_VERSION}")
root.geometry("600x500")
root.resizable(False, False)

input_path = tk.StringVar()
output_path = tk.StringVar()
bitrate_480 = tk.StringVar()
bitrate_720 = tk.StringVar()
bitrate_1080 = tk.StringVar()
progress_var = tk.IntVar()

cfg = load_config()
input_path.set(cfg.get("input", ""))
output_path.set(cfg.get("output", ""))
bitrate_480.set(cfg.get("bitrates", {}).get("480p", "800"))
bitrate_720.set(cfg.get("bitrates", {}).get("720p", "2500"))
bitrate_1080.set(cfg.get("bitrates", {}).get("1080p", "5000"))

tk.Label(root, text="MP4-файл").pack(anchor="w", padx=10, pady=(10,0))
tk.Entry(root, textvariable=input_path, width=70).pack(padx=10)
tk.Button(root, text="Выбрать файл", command=browse_input).pack(pady=(5, 15))

tk.Label(root, text="Папка для вывода").pack(anchor="w", padx=10)
tk.Entry(root, textvariable=output_path, width=70).pack(padx=10)
tk.Button(root, text="Выбрать папку", command=browse_output).pack(pady=(5, 15))

frame = tk.LabelFrame(root, text="Настройки битрейта", padx=10, pady=10)
frame.pack(padx=15, pady=10, fill="x")

tk.Label(frame, text="480p").grid(row=0, column=0, sticky="e")
tk.Entry(frame, textvariable=bitrate_480, width=10).grid(row=0, column=1)
tk.Label(frame, text="Kbps").grid(row=0, column=2, sticky="w")

tk.Label(frame, text="720p").grid(row=1, column=0, sticky="e")
tk.Entry(frame, textvariable=bitrate_720, width=10).grid(row=1, column=1)
tk.Label(frame, text="Kbps").grid(row=1, column=2, sticky="w")

tk.Label(frame, text="1080p").grid(row=2, column=0, sticky="e")
tk.Entry(frame, textvariable=bitrate_1080, width=10).grid(row=2, column=1)
tk.Label(frame, text="Kbps").grid(row=2, column=2, sticky="w")

tk.Button(root, text="Конвертировать", command=run_conversion).pack(pady=10)
ttk.Progressbar(root, variable=progress_var, maximum=100, length=500).pack(padx=20)

status_label = tk.Label(root, text="", font=("Segoe UI", 10, "bold"))
status_label.pack(pady=10)

check_for_update()
root.mainloop()
