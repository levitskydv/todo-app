from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2
from psycopg2 import OperationalError

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Database connection function
def get_db_connection():
    try:
        conn = psycopg2.connect(
            dbname="todo_db",
            user="todo_user",
            password="todo_password",
            host="db"
        )
        return conn
    except OperationalError as e:
        print(f"Error connecting to the database: {e}")
        return None

# Create table if it doesn't exist
def initialize_db():
    conn = get_db_connection()
    if conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS todos (
                    id SERIAL PRIMARY KEY,
                    task TEXT NOT NULL
                );
            """)
            conn.commit()
        conn.close()

# Initialize the database when the app starts
initialize_db()

@app.route('/todos', methods=['GET'])
def get_todos():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    with conn.cursor() as cur:
        cur.execute("SELECT * FROM todos;")
        todos = cur.fetchall()
    conn.close()

    # Format the response
    todos_list = [{"id": todo[0], "task": todo[1]} for todo in todos]
    return jsonify(todos_list)

@app.route('/todos', methods=['POST'])
def add_todo():
    task = request.json.get('task')
    if not task:
        return jsonify({"error": "Task is required"}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    with conn.cursor() as cur:
        cur.execute("INSERT INTO todos (task) VALUES (%s);", (task,))
        conn.commit()
    conn.close()

    return jsonify({"message": "Todo added!"}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=30081)