from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

# Initialize database
def init_db():
    conn = sqlite3.connect("users.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT,
            age INTEGER,
            color TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        age = int(request.form["age"])
        color = request.form["color"]

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, password, age, color) VALUES (?, ?, ?, ?)",
            (username, password, age, color)
        )
        conn.commit()
        conn.close()

        return redirect("/")

    # Fetch users to display
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT username, age, color FROM users")
    users = cursor.fetchall()
    #print(users)
    conn.close()

    return render_template("index.html", users=users)

if __name__ == "__main__":
    # Use debug=True for automatic reload on code changes
    #app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

