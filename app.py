from flask import Flask, render_template, request, redirect
import psycopg2
import psycopg2.extras
import os

app = Flask(__name__)

DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    DATABASE_URL = "postgres://flaskuser2:a1234@localhost:5432/flaskdb"

def get_conn():
    return psycopg2.connect(DATABASE_URL)

def init_db():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username TEXT,
            password TEXT,
            age INTEGER,
            color TEXT
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()

init_db()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        age = int(request.form["age"])
        color = request.form["color"]

        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, password, age, color) VALUES (%s, %s, %s, %s)",
            (username, password, age, color)
        )
        conn.commit()
        cursor.close()
        conn.close()

        return redirect("/")

    conn = get_conn()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    #cursor.execute("delete from users")
    cursor.execute("SELECT username, age, color FROM users")
    #conn.commit()
    #conn.close()
    #return
    users = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template("index.html", users=users)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
