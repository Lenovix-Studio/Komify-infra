import requests
import os
import time
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox
import re


class ImageDownloaderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Komify Image Downloader - Upgraded")
        self.root.geometry("650x600")
        self.root.configure(bg="#f5f5f5")

        # Target simpan utama
        self.root_save_path = r"D:\komify-server\tools\output"

        # --- UI LAYOUT ---
        # Label & Input URL (Perbaikan padx di sini)
        tk.Label(
            root,
            text="Masukkan Link Gambar Pixiv (URL i.pximg.net):",
            font=("Arial", 10, "bold"),
            bg="#f5f5f5",
        ).pack(pady=(15, 0), anchor="w", padx=20)
        self.entry_url = tk.Entry(root, width=75, font=("Courier New", 9))
        self.entry_url.pack(pady=5, padx=20)
        self.entry_url.insert(
            0,
            "https://i.pximg.net/img-original/img/2024/06/11/21/59/34/119113011-70e4c543f8d3338aa8ab53c4b3faae0c_p0.jpg",
        )

        # Label & Input Folder (Perbaikan padx di sini)
        tk.Label(
            root,
            text="Nama Folder Kustom (Kosongkan untuk otomatis menggunakan ID):",
            font=("Arial", 10),
            bg="#f5f5f5",
        ).pack(pady=(10, 0), anchor="w", padx=20)
        self.entry_folder = tk.Entry(root, width=75, font=("Courier New", 9))
        self.entry_folder.pack(pady=5, padx=20)

        # Kontrol Tombol (Frame)
        btn_frame = tk.Frame(root, bg="#f5f5f5")
        btn_frame.pack(pady=15)

        self.btn_download = tk.Button(
            btn_frame,
            text="Mulai Download",
            command=self.start_thread,
            bg="#2ecc71",
            fg="white",
            font=("Arial", 10, "bold"),
            width=18,
            relief="flat",
        )
        self.btn_download.grid(row=0, column=0, padx=5)

        self.btn_open_folder = tk.Button(
            btn_frame,
            text="Buka Folder Output",
            command=self.open_output_folder,
            bg="#3498db",
            fg="white",
            font=("Arial", 10),
            width=18,
            relief="flat",
        )
        self.btn_open_folder.grid(row=0, column=1, padx=5)

        # Log Area (Perbaikan padx di sini)
        tk.Label(
            root, text="Log Aktivitas:", font=("Arial", 9, "bold"), bg="#f5f5f5"
        ).pack(anchor="w", padx=20)
        self.log_area = scrolledtext.ScrolledText(
            root,
            width=80,
            height=18,
            font=("Courier New", 9),
            bg="#2c3e50",
            fg="#ecf0f1",
        )
        self.log_area.pack(pady=5, padx=20)

    def write_log(self, message):
        """Thread-safe logging menggunakan root.after"""
        self.root.after(0, self._safe_write_log, message)

    def _safe_write_log(self, message):
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.see(tk.END)

    def update_btn_state(self, state, text=None, bg_color=None):
        """Thread-safe untuk mengubah status tombol"""

        def change():
            if state is not None:
                self.btn_download.config(state=state)
            if text is not None:
                self.btn_download.config(text=text)
            if bg_color is not None:
                self.btn_download.config(bg=bg_color)

        self.root.after(0, change)

    def open_output_folder(self):
        """Membuka folder output di Windows Explorer"""
        if os.path.exists(self.root_save_path):
            os.startfile(self.root_save_path)
        else:
            messagebox.showwarning(
                "Warning",
                "Folder output belum dibuat. Silakan download terlebih dahulu.",
            )

    def start_thread(self):
        self.update_btn_state(tk.DISABLED, "Mengunduh...", "#e67e22")
        thread = threading.Thread(target=self.process_download, daemon=True)
        thread.start()

    def download_file(self, url, headers, target_path):
        """Mengunduh gambar secara streaming untuk efisiensi memori"""
        try:
            with requests.get(url, headers=headers, timeout=10, stream=True) as res:
                if res.status_code == 200:
                    with open(target_path, "wb") as f:
                        for chunk in res.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)
                    return True
        except Exception:
            pass
        return False

    def process_download(self):
        full_url = self.entry_url.get().strip()
        custom_folder = self.entry_folder.get().strip()

        if not full_url:
            self.write_log("Error: Link tidak boleh kosong!")
            self.update_btn_state(tk.NORMAL, "Mulai Download", "#2ecc71")
            return

        try:
            target_file = full_url.rsplit("/", 1)[1]
            base_url = full_url.rsplit("/", 1)[0] + "/"

            match = re.search(r"^(\d+)", target_file)
            if not match:
                self.write_log("Error: Format ID tidak ditemukan dalam URL.")
                self.update_btn_state(tk.NORMAL, "Mulai Download", "#2ecc71")
                return

            image_id_clean = match.group(1)
            start_id = int(image_id_clean)
            folder_name = custom_folder if custom_folder else image_id_clean

            subfolder_path = os.path.join(self.root_save_path, folder_name)
            if not os.path.exists(subfolder_path):
                os.makedirs(subfolder_path)

            self.write_log(f"--- Folder Tujuan: {subfolder_path} ---")
            self.write_log(
                f"--- Memulai Proses Scan & Download ID: {image_id_clean} ---"
            )

            headers = {
                "Referer": "https://www.pixiv.net/",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            }

            current_id = start_id

            while True:
                found_any_in_id = False
                page = 0

                while True:
                    if page == 0 and current_id == start_id:
                        base_filename = target_file.rsplit(".", 1)[0]
                    else:
                        base_filename = f"{current_id}_p{page}"

                    success = False

                    for ext in [".jpg", ".png", ".jpeg"]:
                        test_filename = (
                            f"{base_filename}{ext}"
                            if "." not in base_filename
                            else base_filename
                        )
                        if page > 0 or current_id != start_id:
                            test_filename = f"{current_id}_p{page}{ext}"

                        url = base_url + test_filename
                        self.write_log(f"Mengecek: {test_filename}...")

                        file_path = os.path.join(subfolder_path, test_filename)
                        if self.download_file(url, headers, file_path):
                            self.write_log(f" -> Berhasil Diunduh: {test_filename}")
                            success = True
                            break

                    if success:
                        found_any_in_id = True
                        page += 1
                        time.sleep(0.5)
                    else:
                        if page == 0 and "_" in base_filename and "-" in base_filename:
                            target_file = f"{current_id}_p0.jpg"
                            continue

                        self.write_log(
                            f" Selesai/Tidak ditemukan pada halaman: p{page}"
                        )
                        break

                if not found_any_in_id:
                    self.write_log(
                        "\n--- Semua ID Berhasil Di-scan / Proses Selesai ---"
                    )
                    break

                current_id += 1

        except Exception as e:
            self.write_log(f"Kesalahan Sistem: {e}")

        self.update_btn_state(tk.NORMAL, "Mulai Download", "#2ecc71")


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageDownloaderGUI(root)
    root.mainloop()
