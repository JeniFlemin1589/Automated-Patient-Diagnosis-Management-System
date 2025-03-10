import sqlite3

def init_db():
    db_file = 'patients.db'

    tables_sql = """
    CREATE TABLE IF NOT EXISTS patients (
        patient_id TEXT PRIMARY KEY,
        name TEXT,
        age INTEGER,
        gender TEXT,
        medical_report_path TEXT,
        diagnosis_letter_path TEXT
    );
    """

    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute(tables_sql)
        print("Database initialized successfully!")

if __name__ == '__main__':
    init_db()
