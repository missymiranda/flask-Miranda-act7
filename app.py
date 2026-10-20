from flask import Flask, jsonify, request, render_template
import sqlite3
from pathlib import Path

app = Flask(__name__)

# ==========================================
# DATABASE CONFIGURATION
# ==========================================

DB_PATH = Path(__file__).with_name("students.db")


def get_db_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


# ==========================================
# HOMEPAGE - YOUR WEBSITE DESIGN
# ==========================================

@app.route('/')
def home():
    return render_template('index.html')


# ==========================================
# ORIGINAL STUDENT API
# ==========================================

@app.route('/student')
def get_student():
    return jsonify({
        "student_id": "2024-00076",
        "name": "Missy Miranda",
        "program": "BSIT",
        "year": 3,
        "section": "3B"
    })


# ==========================================
# HELLO API
# ==========================================

@app.route('/hello')
def say_hello():
    name = request.args.get('name', 'Student')
    return jsonify({
        "message": f"Hello, {name}!"
    })


# ==========================================
# CAMPUS API
# ==========================================

@app.route('/campus')
def get_campus():
    return jsonify({
        "campus": "San Enrique-Campus",
        "location": "Iloilo",
        "status": "Open",
        "type": "University Campus"
    })


# ==========================================
# GRADE API
# ==========================================

@app.route('/grade')
def get_grade():
    return jsonify({
        "subject": "IT 3120",
        "grade": 95,
        "remarks": "Passed"
    })


# ==========================================
# GET ALL STUDENTS FROM DATABASE
# ==========================================

@app.route('/students')
def get_all_students():
    connection = get_db_connection()

    try:
        students = connection.execute(
            'SELECT * FROM students ORDER BY id'
        ).fetchall()

        return jsonify([dict(student) for student in students])

    except sqlite3.Error:
        app.logger.exception("Error retrieving students")
        return jsonify({"error": "Could not retrieve students"}), 500

    finally:
        connection.close()


# ==========================================
# GET STUDENT BY DATABASE ID
# Example: /students/1
# ==========================================

@app.route('/students/<int:id>')
def get_student_by_id(id):
    connection = get_db_connection()

    try:
        student = connection.execute(
            'SELECT * FROM students WHERE id = ?',
            (id,)
        ).fetchone()

        if student is None:
            return jsonify({"error": "Student not found"}), 404

        return jsonify(dict(student))

    except sqlite3.Error:
        app.logger.exception("Error retrieving student")
        return jsonify({"error": "Could not retrieve student"}), 500

    finally:
        connection.close()


# ==========================================
# FILTER STUDENTS BY PROGRAM
# Example: /students/program/BSIT
# ==========================================

@app.route('/students/program/<program>')
def get_students_by_program(program):
    connection = get_db_connection()

    try:
        students = connection.execute(
            '''
            SELECT * FROM students
            WHERE LOWER(program) = LOWER(?)
            ORDER BY id
            ''',
            (program,)
        ).fetchall()

        return jsonify([dict(student) for student in students])

    except sqlite3.Error:
        app.logger.exception("Error filtering students")
        return jsonify({"error": "Could not filter students"}), 500

    finally:
        connection.close()


# ==========================================
# RUN APPLICATION
# ==========================================

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
