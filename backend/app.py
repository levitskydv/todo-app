from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Database connection
conn = psycopg2.connect(
    dbname="todo_db",
    user="todo_user",
    password="todo_password",
    host="db"
)

# Create table
with conn.cursor() as cur:
    cur.execute("""
        CREATE TABLE IF NOT EXISTS todos (
            id SERIAL PRIMARY KEY,
            task TEXT NOT NULL
        );
    """)
    conn.commit()

@app.route('/todos', methods=['GET'])
def get_todos():
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM todos;")
        todos = cur.fetchall()
    return jsonify(todos)

@app.route('/todos', methods=['POST'])
def add_todo():
    task = request.json.get('task')
    with conn.cursor() as cur:
        cur.execute("INSERT INTO todos (task) VALUES (%s);", (task,))
        conn.commit()
    return jsonify({"message": "Todo added!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)