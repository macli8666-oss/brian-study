import sqlite3
import json
from app.config import DATABASE_PATH


def get_db():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS user_progress (
            user_id TEXT NOT NULL,
            subject TEXT NOT NULL,
            chapter_id TEXT NOT NULL,
            point_index INTEGER DEFAULT 0,
            completed INTEGER DEFAULT 0,
            PRIMARY KEY (user_id, subject, chapter_id)
        );

        CREATE TABLE IF NOT EXISTS quiz_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            subject TEXT NOT NULL,
            chapter_id TEXT NOT NULL,
            question_index INTEGER NOT NULL,
            selected TEXT,
            correct TEXT,
            is_correct INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS user_state (
            user_id TEXT PRIMARY KEY,
            current_subject TEXT,
            current_chapter TEXT,
            current_mode TEXT,
            current_index INTEGER DEFAULT 0
        );
    """)
    conn.commit()
    conn.close()


def get_user_state(user_id):
    conn = get_db()
    row = conn.execute("SELECT * FROM user_state WHERE user_id = ?", (user_id,)).fetchone()
    conn.close()
    if row:
        return dict(row)
    return None


def set_user_state(user_id, subject=None, chapter=None, mode=None, index=0):
    conn = get_db()
    conn.execute("""
        INSERT INTO user_state (user_id, current_subject, current_chapter, current_mode, current_index)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(user_id) DO UPDATE SET
            current_subject = ?,
            current_chapter = ?,
            current_mode = ?,
            current_index = ?
    """, (user_id, subject, chapter, mode, index, subject, chapter, mode, index))
    conn.commit()
    conn.close()


def save_quiz_result(user_id, subject, chapter_id, question_index, selected, correct, is_correct):
    conn = get_db()
    conn.execute("""
        INSERT INTO quiz_results (user_id, subject, chapter_id, question_index, selected, correct, is_correct)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (user_id, subject, chapter_id, question_index, selected, correct, is_correct))
    conn.commit()
    conn.close()


def get_wrong_questions(user_id, subject=None, chapter_id=None):
    conn = get_db()
    query = "SELECT * FROM quiz_results WHERE user_id = ? AND is_correct = 0"
    params = [user_id]
    if subject:
        query += " AND subject = ?"
        params.append(subject)
    if chapter_id:
        query += " AND chapter_id = ?"
        params.append(chapter_id)
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_quiz_stats(user_id, subject=None):
    conn = get_db()
    query = "SELECT COUNT(*) as total, SUM(is_correct) as correct FROM quiz_results WHERE user_id = ?"
    params = [user_id]
    if subject:
        query += " AND subject = ?"
        params.append(subject)
    row = conn.execute(query, params).fetchone()
    conn.close()
    return dict(row)
