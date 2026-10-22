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
            ("SEC-2024-001", "Karol Vincent Pedregosa", "BSA", 4, "A"),
            ("SEC-2024-002", "Rizza Anthea Miranda", "BSIT", 2, "B"),
            ("SEC-2024-003", "Issah Kailah Javier", "BSCS", 2, "A"),
            ("SEC-2024-004", "John Parker", "BSHM", 3, "C"),
            ("SEC-2024-005", "Alexaandra Cruzr", "BSED", 4, "B"),
            ("SEC-2024-006", "Kate Santos", "BSOA", 1, "C")
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
