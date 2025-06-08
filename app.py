from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# --- DATABASE CONFIGURATION ---
DB_NAME = "-hidden" # Add yours
DB_USER = "-hidden" # Add yours
DB_PASSWORD = "-hidden-" # Add yours
DB_HOST = "-hidden-" # Add yours
DB_PORT = "5432" # Add yours
TABLE_NAME = "marvel_dc" # Add yours

def get_db_connection():
    """Establishes a connection to the PostgreSQL database."""
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        return conn
    except psycopg2.Error as e:
        print(f"Error connecting to database: {e}")
        return None

@app.route('/data', methods=['GET'])
def get_data():
    """Fetches all data from the specified table."""
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cur = conn.cursor()
        cur.execute(f"SELECT id, movie, year, genre, runtime, description, imdb_score FROM {TABLE_NAME}")
        colnames = [desc[0] for desc in cur.description]
        rows = cur.fetchall()
        data = [dict(zip(colnames, row)) for row in rows]
        cur.close()
        conn.close()
        return jsonify(data)
    except psycopg2.Error as e:
        print(f"Error fetching data: {e}")
        if conn:
            conn.rollback()
            cur.close()
            conn.close()
        return jsonify({"error": f"Failed to fetch data: {e}"}), 500
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        if conn:
            conn.rollback()
            cur.close()
            conn.close()
        return jsonify({"error": f"An unexpected error occurred: {e}"}), 500

@app.route('/add', methods=['POST'])
def add_data():
    """Adds a new movie record to the table."""
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        data = request.get_json()
        required_fields = ['id', 'movie', 'year', 'genre', 'runtime', 'description', 'imdb_score']
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400

        cur = conn.cursor()
        sql = f"""
            INSERT INTO {TABLE_NAME} (id, movie, year, genre, runtime, description, imdb_score)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cur.execute(sql, (
            data['id'], data['movie'], data['year'], data['genre'],
            data['runtime'], data['description'], data['imdb_score']
        ))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "Data added successfully"}), 201
    except psycopg2.Error as e:
        print(f"Error adding data: {e}")
        if conn:
            conn.rollback()
            cur.close()
            conn.close()
        return jsonify({"error": f"Failed to add data: {e}"}), 500
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        if conn:
            conn.rollback()
            cur.close()
            conn.close()
        return jsonify({"error": f"An unexpected error occurred: {e}"}), 500

@app.route('/delete/<int:item_id>', methods=['DELETE'])
def delete_data(item_id):
    """Deletes a record from the table based on its ID."""
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cur = conn.cursor()
        sql = f"DELETE FROM {TABLE_NAME} WHERE id = %s"
        cur.execute(sql, (item_id,))

        if cur.rowcount == 0:
            conn.rollback()
            cur.close()
            conn.close()
            return jsonify({"error": f"Item with ID {item_id} not found"}), 404

        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": f"Data with ID {item_id} deleted successfully"}), 200
    except psycopg2.Error as e:
        print(f"Error deleting data: {e}")
        if conn:
            conn.rollback()
            cur.close()
            conn.close()
        return jsonify({"error": f"Failed to delete data: {e}"}), 500
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        if conn:
            conn.rollback()
            cur.close()
            conn.close()
        return jsonify({"error": f"An unexpected error occurred: {e}"}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)