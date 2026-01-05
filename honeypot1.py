import time
import sqlite3
from gabungan import sql_injection

# Membuat database + tabel otomatis 
con = sqlite3.connect("honey01.db")

#Membuat cursor eksekusi query  
cursor = con.cursor()

#Membuat tabel log
cursor.execute ("""
CREATE TABLE IF NOT EXISTS logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    waktu TEXT,
    status TEXT,
    inputan TEXT
)
""")
con.commit()

print("---- DRAFT HONEYPOT LOGIN -----")
print("Sistem ini sedang memantau input mencurigakan ....\n")
# untuk terus memantau input
while True:
    user_input = input("Masukkan Username/Query/...:  ").strip()

    # Jika input = keluar → berhenti
    if user_input.lower() == "keluar":
        print("Program dihentikan.")
        break   

    # Pengecekan SQL Injection
    if sql_injection(user_input):
        status = "SQL INJECTION ATTEMPT"
        print("Input Mencurigakan! \n")
    else:
        status = "NORMAL INPUT"
        print("Input Aman.\n")

    # Simpan ke file log → Masuk setiap input
    with open("honey.txt", "a") as log:
        log.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {status} - {user_input}\n")

    print("Input dicatat → lihat file honey.txt\n")

    # Simpan ke Sqlite
    cursor.execute(
         "INSERT INTO logs (waktu, status, inputan) VALUES (?, ?, ?)",
         (time.strftime('%Y-%m-%d %H:%M:%S'), status, user_input)
    )
    con.commit()
    print("Input dicatat → lihat honey.txt / honey.db\n")