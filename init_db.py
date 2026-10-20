import sqlite3
from pathlib import Path

# Locate the database beside this Python file
DB_PATH = Path(__file__).with_name("students.db")


def initialize_database():
    connection = sqlite3.connect(DB_PATH)

    try:
        cursor = connection.cursor()

        # Create the students table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT NOT NULL,
                name TEXT NOT NULL,
                program TEXT NOT NULL,
                year INTEGER NOT NULL,
                section TEXT NOT NULL
            )
        """)

        # Reset the sample data for this activity
        cursor.execute("DELETE FROM students")
        cursor.execute(
            "DELETE FROM sqlite_sequence WHERE name = 'students'"
        )

        # Fictional sample student records
        student_records = [
            ("ISU-2026-201", "Avery Bennett", "BSIT", 1, "A"),
            ("ISU-2026-202", "Riley Morgan", "BSIT", 2, "B"),
            ("ISU-2026-203", "Jordan Ellis", "BSCS", 2, "A"),
            ("ISU-2026-204", "Cameron Blake", "BSIT", 3, "C"),
            ("ISU-2026-205", "Quinn Parker", "BSCS", 4, "B"),
            ("ISU-2026-206", "Dakota Reed", "BSOA", 1, "C")
        ]

        cursor.executemany("""
            INSERT INTO students (
                student_id, name, program, year, section
            )
            VALUES (?, ?, ?, ?, ?)
        """, student_records)

        connection.commit()
        print("Database created successfully.")
        print(f"Inserted {len(student_records)} sample student records.")

    except sqlite3.Error:
        connection.rollback()
        raise

    finally:
        connection.close()


if __name__ == "__main__":
    initialize_database()
