import os

def command_line():
    commandList = {
        "clear": lambda: os.system("clear" if os.name == "posix" else "cls"),
        "cd": lambda path: os.chdir(path) if os.path.exists(path) else print("Direktori tidak ditemukan"),
        "pwd": lambda: print(os.getcwd()),
        "ls": lambda: os.system("ls" if os.name == "posix" else "dir"),
    }

    while True:
        try:
            current_dir = os.getcwd()
            commandLine = input(f"{current_dir} > ").lower().split()
            if commandLine[0] in commandList:
                if len(commandLine) > 1:
                  commandList[commandLine[0]](commandLine[1])
                else:
                    if commandLine[0] != "cd":
                    commandList[commandLine[0]]()
                    else:
                        print("Masukkan direktori yang ingin dituju")
            else:
                print("Perintah tidak dikenal")
        except Exception as e:
            print(f"Error: {e}")

def main():
    command_line()

if __name__ == "__main__":
    main()