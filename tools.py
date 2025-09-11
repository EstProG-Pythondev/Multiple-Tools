import os
import sys
import time
import shutil
import string
import random

class LoadingAnimation:
    def __init__(self, text="Loading", duration=2):
        self.text = text
        self.duration = duration
        self.animation = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]

    def run(self):    
        end_time = time.time() + self.duration    
        i = 0    
        while time.time() < end_time:    
            sys.stdout.write(f"\r{self.text} {self.animation[i % len(self.animation)]}")    
            sys.stdout.flush()    
            time.sleep(0.1)    
            i += 1    
        sys.stdout.write("\r" + " " * (len(self.text) + 4) + "\r")


class BackupManager:
    def __init__(self, backup_path="/sdcard/backupFolderFile"):
        self.backup_path = backup_path

    def ensure_backup_dir(self):    
        LoadingAnimation("check direktori backup", 2).run()    
        if not os.path.exists(self.backup_path):    
            print("direktori tidak ditemukan ❌")    
            LoadingAnimation("membuat direktori backup...", 2).run()    
            os.makedirs(self.backup_path)    
            print("direktori berhasil dibuat")    
        else:    
            print("direktori ditemukan ✅")    

    def backup(self):    
        self.ensure_backup_dir()    
        path = input("Masukkan path file/folder yang ingin dibackup: ").strip()    
        LoadingAnimation("checking", 1.5).run()    

        try:    
            if os.path.isfile(path):    
                self._backup_file(path)    
            elif os.path.isdir(path):    
                self._backup_folder(path)    
            else:    
                print(f"❌ Path '{path}' tidak ditemukan.")    
        except Exception as e:    
            print(f"⚠️ Error saat backup: {e}")    

        input("\nTekan ENTER untuk kembali ke menu...")    

    def _backup_file(self, path):    
        target = os.path.join(self.backup_path, os.path.basename(path))    
        if os.path.exists(target):    
            choice = input("⚠️ File sudah ada di backup, timpa? (yes/no): ")    
            if choice.lower() == "yes":    
                LoadingAnimation("Membackup file...", 2).run()    
                shutil.copy(path, target)    
                print("✅ File berhasil dibackup!")    
            else:    
                print("Backup dibatalkan")    
        else:    
            LoadingAnimation("Membackup file...", 2).run()    
            shutil.copy(path, target)    
            print("✅ File berhasil dibackup!")    

    def _backup_folder(self, path):    
        target = os.path.join(self.backup_path, os.path.basename(path))    
        if os.path.exists(target):    
            choice = input("⚠️ Folder sudah ada di backup, timpa? (yes/no): ")    
            if choice.lower() == "yes":    
                LoadingAnimation("Membackup folder...", 2).run()    
                shutil.rmtree(target)    
                shutil.copytree(path, target)    
                print("✅ Folder berhasil dibackup!")    
            else:    
                print("Backup dibatalkan")    
        else:    
            LoadingAnimation("Membackup folder...", 2).run()    
            shutil.copytree(path, target)    
            print("✅ Folder berhasil dibackup!")


class PasswordGenerator:
    def generate(self):
        try:
            length = int(input("Masukkan panjang password: "))
            if 8 <= length <= 30:
                chars = string.ascii_letters + string.digits + string.punctuation
                LoadingAnimation("Membuat password...", 2).run()
                passwd = ''.join(random.choice(chars) for _ in range(length))
                print(f"🔑 Password baru kamu: {passwd}")
            elif length > 30:
                print("❌ Panjang password maksimal 30 karakter.")
            else:
                print("❌ Panjang password minimal 8 karakter.")
        except ValueError:
            print("❌ Input harus berupa angka.")
        except Exception as e:
            print(f"⚠️ Error: {e}")
        input("\nTekan ENTER untuk kembali ke menu...")


class App:
    def __init__(self):
        self.backup_manager = BackupManager()
        self.password_generator = PasswordGenerator()

    def run(self):    
        while True:    
            os.system("clear" if os.name == "posix" else "cls")    
            print("="*40)    
            print(" 📌 PROGRAM MULTIFUNGSI (OOP)")    
            print("="*40)    
            print("1. Generate Password")    
            print("2. Backup File/Folder")    
            print("3. Keluar")    
            print("="*40)    

            try:    
                choice = int(input("Pilih menu (1-3): "))    
                if choice == 1:    
                    self.password_generator.generate()    
                elif choice == 2:    
                    self.backup_manager.backup()    
                elif choice == 3:    
                    print("👋 Keluar dari program...")    
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


if __name__ == "__main__":
    App().run()
