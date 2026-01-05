from flask import Flask, render_template, request
import sqlite3
import time
from gabungan import sql_injection

app = Flask(__name__)

#login halaman
@app.route("/login", methods=["GET", "POST"])
def login():
    status = None

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if sql_injection(username) or sql_injection(password):
            status = "SQL INJECTION ATTEMPT"
        else:
            status = "NORMAL INPUT"

        waktu = time.strftime('%Y-%m-%d %H:%M:%S')

        # simpan ke txt
        with open("honey.txt", "a") as f:
            f.write(f"[{waktu}] {status} - {username} | {password}\n")

        # simpan ke sqlite
        con = sqlite3.connect("honey01.db")
        cur = con.cursor()
        cur.execute(
            "INSERT INTO logs (waktu, status, inputan) VALUES (?, ?, ?)",
            (waktu, status, f"{username} | {password}")
        )
        con.commit()
        con.close()

    return render_template("login.html", status=status)

# if __name__ == "__main__":
#     app.run(debug=True)

# admin halaman
@app.route("/admin")
def admin():

    con = sqlite3.connect("honey01.db")
    cur = con.cursor()

    cur.execute("SELECT COUNT(*) FROM logs")
    total = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM logs WHERE status='SQL INJECTION ATTEMPT'")
    sqli = cur.fetchone()[0]

    con.close()

    persen = 0 if total == 0 else round((sqli / total) * 100, 2)

    return render_template("admin.html", sqli=sqli, persen=persen)
# run server
if __name__ == "__main__":
    app.run(debug=True)