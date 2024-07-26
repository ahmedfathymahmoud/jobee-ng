
import sqlite3
from lib.telegramBot.telegramJobee import tele_jobee
from lib.sources.linkedin import LinkedinAPI


def get_source(source_name):
    if source_name == 'LinkedIn':
        return LinkedinAPI()

    else:
        raise ValueError(f"No support available for {source_name}")

def get_bot(destination):
    if 'telegram' in destination:
        return tele_jobee(destination['telegram']['channel_id'])
    else:
        raise ValueError(f"No bot available for {destination}")

def generate_message(source_name, job):
    if source_name == 'LinkedIn':
        return f'https://www.linkedin.com/jobs/view/{job['entityUrn'].split(':')[-1]}'

    else:
        raise ValueError(f"No support available for {source_name}")


def create_table(conn):
    conn.execute('''CREATE TABLE IF NOT EXISTS jobs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        jobid TEXT NOT NULL UNIQUE
                    );''')
    conn.commit()

def insert_job(conn, jobid):
    conn.execute('INSERT INTO jobs (jobid) VALUES (?)', (jobid,))
    conn.commit()

def job_exists(conn, jobid):
    cursor = conn.execute('SELECT 1 FROM jobs WHERE jobid = ?', (jobid,))
    return cursor.fetchone() is not None