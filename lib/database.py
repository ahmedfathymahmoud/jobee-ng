import sqlite3

def get_db_connection():
    conn = sqlite3.connect('jobs.db')
    conn.row_factory = sqlite3.Row
    return conn


def ensure_table_exists(table_name):
    conn = get_db_connection()
    with conn:
        conn.execute(f'''
            CREATE TABLE IF NOT EXISTS {table_name} (
                id TEXT PRIMARY KEY,
                posted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
    conn.close()

def job_already_posted(job_id, table_name):
    conn = get_db_connection()
    result = conn.execute(
        f'SELECT 1 FROM {table_name} WHERE id = ?', (job_id,)
    ).fetchone()
    conn.close()
    return result is not None

def save_posted_job(job_id,  table_name):
    conn = get_db_connection()
    with conn:
        conn.execute(
            f'INSERT INTO {table_name} (id) VALUES (?)',
            (job_id,)
        )
    conn.close()
