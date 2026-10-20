from flask import Flask, jsonify, request, render_template
import sqlite3
from pathlib import Path

app = Flask(__name__)

DB_PATH = Path(__file__).with_name("students.db")


def get_db_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


# Homepage: display your website design
@app.route('/')
def home():
    return render_template('index.html')


# Get one student
@app.route('/student')
def get_student():
    return jsonify({
        "student_id": "2026-00076",
        "name": "Missy Miranda",
        "program": "BSIT",
        "year": 3,
        "section": "3B"
    })


# Greeting API
@app.route('/hello')
def say_hello():
    name = request.args.get('name', 'Student')
    return jsonify({"message": f"Hello, {name}!"})


# Campus API
@app.route('/campus')
def get_campus():
    return jsonify({
        "campus": "San Enrique-Campus",
        "location": "Iloilo",
        "status": "Open",
        "type": "University Campus"
    })


# Grade API
@app.route('/grade')
def get_grade():
    return jsonify({
        "subject": "IT 3120",
        "grade": 95,
        "remarks": "Passed"
    })


# Get all students
@app.route('/students')
def get_all_students():
    connection = get_db_connection()
    try:
        students = connection.execute(
            'SELECT * FROM students ORDER BY id'
        ).fetchall()
        return jsonify([dict(student) for student in students])
    except sqlite3.Error:
        app.logger.exception("Unable to retrieve students")
        return jsonify({"error": "Database query failed"}), 500
    finally:
        connection.close()


# Get student by database ID
@app.route('/students/<int:id>')
def get_student_by_id(id):
    connection = get_db_connection()
    try:
        student = connection.execute(
            'SELECT * FROM students WHERE id = ?', (id,)
        ).fetchone()

        if student is None:
            return jsonify({"error": "Student not found"}), 404

        return jsonify(dict(student))
    except sqlite3.Error:
        app.logger.exception("Unable to retrieve student")
        return jsonify({"error": "Database query failed"}), 500
    finally:
        connection.close()


# Filter students by program
@app.route('/students/program/<program>')
def get_students_by_program(program):
    connection = get_db_connection()
    try:
        students = connection.execute(
            '''SELECT * FROM students
               WHERE LOWER(program) = LOWER(?)
               ORDER BY id''',
            (program,)
        ).fetchall()
        return jsonify([dict(student) for student in students])
    except sqlite3.Error:
        app.logger.exception("Unable to filter students")
        return jsonify({"error": "Database query failed"}), 500
    finally:
        connection.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
