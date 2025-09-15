print("Selamat datang di Mad Libs game!")

nama = input("Masukkan nama: ")
tempat = input("Masukkan tempat: ")
aktivitas = input("Masukkan aktivitas: ")
makanan = input("Masukkan makanan: ")
hewan = input("Masukkan hewan: ")

cerita = f"""
Suatu hari, {nama} pergi ke {tempat} untuk melakukan {aktivitas}. Di sana, {nama} makan {makanan} dan bertemu dengan seekor {hewan} yang lucu.
"""

print(cerita)