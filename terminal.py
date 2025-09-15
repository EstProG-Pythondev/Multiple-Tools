import os
import shutil

def command_line():
    commandList = {
        "clear": lambda: os.system("clear" if os.name == "posix" else "cls"),
        "cd": lambda path: os.chdir(path) if os.path.exists(path) else print("Direktori tidak ditemukan"),
        "pwd": lambda: print(os.getcwd()),
        "ls": lambda: os.system("ls" if os.name == "posix" else "dir"),
        "cp": lambda src, dst: copy_file_or_folder(src, dst),
        "mv": lambda src, dst: move_file_or_folder(src, dst)
    }

    def copy_file_or_folder(src, dst):
        try:
            if os.path.isfile(src):
                shutil.copy(src, dst)
            elif os.path.isdir(src):
                shutil.copytree(src, dst)
            else:
                print(f"cp: cannot stat: '{src}': No such file or directory")
        except Exception as e:
            print(f"Error: {e}")

    def move_file_or_folder(src, dst):
        try:
            shutil.move(src, dst)
        except Exception as e:
            print(f"Error: {e}")

    while True:
        try:
            current_dir = os.getcwd()
            commandLine = input(f"{current_dir} > ").lower().split()
            if commandLine[0] == "exit":
                print("Keluar dari terminal")
                break
            if commandLine[0] in commandList:
                if len(commandLine) > 1:
                    if commandLine[0] in ["cp", "mv"]:
                        if len(commandLine) > 2:
                            commandList[commandLine[0]](commandLine[1], commandLine[2])
                        else:
                            print(f"{commandLine[0]}: missing file operand")
                    else:
                        commandList[commandLine[0]](commandLine[1])
                else:
                    if commandLine[0] not in ["cp", "mv", "cd"]:
                        commandList[commandLine[0]]()
                    elif commandLine[0] == "cd":
                        print("Masukkan direktori yang ingin dituju")
                    else:
                        print(f"{commandLine[0]}: missing file operand")
            else:
                print(f"{commandLine[0]}: command not found")
        except Exception as e:
            print(f"Error: {e}")