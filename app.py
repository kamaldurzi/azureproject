from flask import Flask, request, jsonify, send_from_directory
import os
import pyodbc

app = Flask(__name__, static_folder='static')

conn_str = os.getenv("SQL_CONN_STR")

@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute("SELECT id, task FROM Tasks")
    rows = cursor.fetchall()
    return jsonify([{"id": r[0], "task": r[1]} for r in rows])

@app.route("/api/tasks", methods=["POST"])
def add_task():
    conn = pyodbc.connect(conn_str)
    task = request.json.get("task")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Tasks (task) VALUES (?)", (task,))
    conn.commit()
    return jsonify({"message": "Task added"}), 201

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
