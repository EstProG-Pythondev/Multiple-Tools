import os
import random
import string
import shutil
import time
import sys
import yt_dlp
from terminal import command_line

def loading_animation(text="Loading", duration=2):
    animation = ["⠋","⠙","⠹","⠸","⠼","⠴","⠦","⠧","⠇","⠏"]
    end_time = time.time() + duration
    i = 0
    while time.time() < end_time:
        sys.stdout.write(f"\r{text} {animation[i % len(animation)]}")
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1
    sys.stdout.write("\r" + " " * (len(text) + 4) + "\r")

def backupfile():
    backup_path = "/storage/emulated/0/backupFolderFile"
    time.sleep(1)
    loading_animation("Memeriksa direktori backup")
    time.sleep(0.5)
    if not os.path.exists(backup_path):
        print("❌ Direktori tidak ditemukan")
        loading_animation("Membuat direktori backup...")
        os.makedirs(backup_path)
        print("✅ Direktori berhasil dibuat")
    else:
        print("✅ Direktori ditemukan")
    time.sleep(0.3)
    path = input("Masukkan path file/folder yang ingin dibackup: ").strip()
    loading_animation("Memeriksa path")
    try:
        if os.path.isfile(path):
            target = os.path.join(backup_path, os.path.basename(path))
            if os.path.exists(target):
                choice = input("⚠️ File sudah ada di backup, timpa? (yes/no): ")
                if choice.lower() == "yes":
                    loading_animation("Membackup file...")
                    shutil.copy(path, target)
                    print("✅ File berhasil dibackup!")
                else:
                    print("❌ Backup dibatalkan")
            else:
                loading_animation("Membackup file...")
                shutil.copy(path, target)
                print("✅ File berhasil dibackup!")
        elif os.path.isdir(path):
            target = os.path.join(backup_path, os.path.basename(path))
            if os.path.exists(target):
                choice = input("⚠️ Folder sudah ada di backup, timpa? (yes/no): ")
                if choice.lower() == "yes":
                    loading_animation("Membackup folder...")
                    shutil.rmtree(target)
                    shutil.copytree(path, target)
                    print("✅ Folder berhasil dibackup!")
                else:
                    print("❌ Backup dibatalkan")
            else:
                loading_animation("Membackup folder...")
                shutil.copytree(path, target)
                print("✅ Folder berhasil dibackup!")
        else:
            print(f"❌ Path '{path}' tidak ditemukan.")
    except Exception as e:
        print(f"⚠️ Error saat backup: {e}")
    input("\nTekan ENTER untuk kembali ke menu...")

def generate_password():
  while True:
    try:
        length = int(input("Masukkan panjang password: "))
        if length < 8 or length > 40:
          print("❌ minimal=8, maximal=40")
          continue
        elif length >= 8 or length <= 30:
          char = string.ascii_letters + string.digits + string.punctuation
          loading_animation("Membuat password...")
          passwd = ''.join(random.choice(char) for _ in range(length))
          print(f"🔑 Password baru kamu: {passwd}")
    except Exception as e:
        print(f"⚠️ Error: {e}")
    input("\nTekan ENTER untuk kembali ke menu...")
    break
def show_yt_dlp_help():
    os.system("clear" if os.name == "posix" else "cls")
    print("="*40)
    print(" 📖 Opsi Populer yt-dlp")
    print("="*40)
    print("-f FORMAT       : Pilih format video (contoh: best, worst, mp4, 720p)")
    print("-o TEMPLATENAME : Output filename template (contoh: '%(title)s.%(ext)s')")
    print("--playlist-items ITEM   : Download item tertentu dari playlist (contoh: 1,3,5-7)")
    print("-a FILE         : Download semua link dari file teks")
    print("--no-playlist   : Hanya download video tunggal, bukan playlist")
    print("--extract-audio : Ekstrak audio saja")
    print("--audio-format FORMAT : Format audio (mp3, wav, dll)")
    print("--merge-output-format FORMAT : Format akhir jika perlu digabung")
    print("="*40)
    input("Tekan ENTER untuk kembali...")

def download_video():
    while True:
        path = input("Masukkan link video, path file, atau ketik 'help' untuk opsi yt-dlp: ").strip()
        if path.lower() == "help":
            show_yt_dlp_help()
            continue

        time.sleep(0.4)
        loading_animation("Memeriksa input")

        if os.path.exists(path) and os.path.isfile(path):
            print(f"✅ File daftar link ditemukan: {path}")
            with open(path, 'r') as f:
                links = f.readlines()
                for link in links:
                    link = link.strip()
                    if link:
                        download_video_from_link(link)
        else:
            print("⚠️ Input dianggap sebagai link langsung...")
            download_video_from_link(path)

        input("\nTekan ENTER untuk kembali ke menu...")
        break

def download_video_from_link(link):
    ydl_opts = {
        'outtmpl': '%(title)s.%(ext)s',
        'format': 'best'
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            loading_animation("Mengunduh video")
            ydl.download([link])
            print("✅ Video berhasil diunduh!")
    except Exception as e:
        print(f"⚠️ Error saat download video: {e}")
        
def creation_games():
  os.system("clear" if os.name == "posix" else "cls")
  print("===========================================")
  print("   Hello, welcome to creation games mode")
  print("===========================================")
  input(">>")
  
def main():
    while True:
        os.system("clear" if os.name == "posix" else "cls")
        print("="*40)
        print(" 📌 PROGRAM MULTIFUNGSI")
        print("="*40)
        print("1. Generate Password")
        print("2. Backup File/Folder")
        print("3. Download Video")
        print("4. Terminal Users")
        print("5. Creation Games")
        print("6. Keluar")
        print("="*40)
        try:
            choice = int(input("Pilih menu (1-6): "))
            if choice == 1:
                generate_password()
            elif choice == 2:
                backupfile()
            elif choice == 3:
                download_video()
            elif choice == 4:
              command_line()
            elif choice == 5:
              creation_games()
            elif choice == 6:
              print("Loading", end='')
              time.sleep(0.7)
              for i in range(5, 0, -1):
                print(".", end='', flush=True)
                time.sleep(0.3)
              print("\nKeluar dari program")
              break
            else:
                print("❌ Pilihan tidak valid.")
                input("\nTekan ENTER untuk coba lagi...")
        except ValueError:
            print("❌ Input harus berupa angka.")
            input("\nTekan ENTER untuk coba lagi...")
        except Exception as e:
            print(f"⚠️ Error: {e}")
            input("\nTekan ENTER untuk coba lagi...")

if __name__ == '__main__':
    main()