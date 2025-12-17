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
            age INTEGER
        )
    """)
    conn.commit()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users2 (
            id SERIAL PRIMARY KEY,
            username TEXT,
            age INTEGER
        )
    """)
    conn.commit()

    cursor.close()
    conn.close()

#init_db()


@app.route("/", methods=["GET", "POST"])
def index():

    def get_tables():
        # ---------- GET ----------
        conn = get_conn()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        # 1️⃣ Get all tables (for combo box)
        cursor.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            ORDER BY table_name
        """)
        tables = cursor.fetchall()
        cursor.close()
        conn.close()
        return tables

    aksyon='none'

    if request.method == "POST":
        selected_table = request.form.get("table")
        print(selected_table)
        action = request.form.get("action")

        conn = get_conn()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        data=[]
        if action == "adduser":
            username = request.form["username"]
            age = int(request.form["age"])
            cursor.execute(
                f"INSERT INTO {selected_table} (username, age) VALUES (%s, %s)",
                (username, age)
            )
            aksyon="adduser"
            print("aksyon ", aksyon)

        elif action == "showusers":
            cursor.execute(f"select username, age from {selected_table}")
            data = cursor.fetchall()
            aksyon="showusers"
            print("aksyon ", aksyon)

        elif action == "delete":
            cursor.execute(f"delete from {selected_table}")
            aksyon="delete"
            print("aksyon ", aksyon)

        elif action == "deletetable":
            cursor.execute(f"drop table if exists {selected_table}")
            aksyon="drop"
            print("aksyon ", aksyon)
            print(f"***{selected_table} dropped***")

        conn.commit()
        cursor.close()
        conn.close()

        if action=='showusers':
            show_results=True
        else:
            show_results=False
    
        #return redirect("/")
        tables=get_tables()
        return render_template(
            "index.html",
            tables=tables,
            selected_table=selected_table,
            data=data,
            show_results=show_results
        )

    tables=get_tables()

    # 2️⃣ Pick default table
    selected_table = request.args.get("table")

    allowed_tables = [t["table_name"] for t in tables]
    if not selected_table and allowed_tables:
        selected_table = allowed_tables[0]
    """
    conn = get_conn()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    # 3️⃣ Load rows from selected table
    data = []
    if selected_table in allowed_tables:
        cursor.execute(f"SELECT * FROM {selected_table}")
        data = cursor.fetchall()

    cursor.close()
    conn.close()
    """
    show_results=request.method=="POST"
    print(show_results)
    return render_template(
        "index.html",
        tables=tables,
        selected_table=selected_table,
        #data=data,
        show_results=request.method=="POST"
    )

if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
