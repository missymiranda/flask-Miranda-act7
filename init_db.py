
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

        # Clear existing sample records
        cursor.execute("DELETE FROM students")
        cursor.execute(
            "DELETE FROM sqlite_sequence WHERE name = 'students'"
        )

        # Fictional sample student records
        student_records = [
            ("2024-0001", "Harper Collins", "BSIT", 1, "A"),
            ("2024-0002", "Logan Mitchell", "BSIT", 2, "B"),
            ("2024-0003", "Skyler Anderson", "BEED", 2, "A"),
            ("2024-0004", "Peyton Brooks", "BSHM", 3, "C"),
            ("2024-0005", "Emerson Bailey", "BSA", 4, "B"),
            ("2024-0006", "Rowan Cooper", "BSOA", 1, "C")
        ]

        # Insert the records into the database
        cursor.executemany("""
            INSERT INTO students (
                student_id,
                name,
                program,
                year,
                section
            )
            VALUES (?, ?, ?, ?, ?)
        """, student_records)

        connection.commit()

        print("Database created successfully.")
        print(
            f"Inserted {len(student_records)} sample student records."
        )

    except sqlite3.Error:
        connection.rollback()
        raise

    finally:
        connection.close()


if __name__ == "__main__":
    initialize_database()
