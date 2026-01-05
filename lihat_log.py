import sqlite3

con = sqlite3.connect("honey01.db")
cursor = con.cursor()

cursor.execute("SELECT * FROM logs")
data = cursor.fetchall()

print("\n=== DATA LOG HONEYPOT ===\n")

for row in data:
    print(f"ID     : {row[0]}")
    print(f"Waktu  : {row[1]}")
    print(f"Status : {row[2]}")
    print(f"Input  : {row[3]}")
    print("-" * 30)

con.close()