import sqlite3 as sq
import pandas as pd

async def create_db():
    print("База данных создана!")

    global db, cur
    db = sq.connect('zayavka.db')
    cur = db.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS users(
        user_id INTEGER PRIMARY KEY,
        username TEXT
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS events(
        event_id INTEGER PRIMARY KEY,
        event_photo TEXT,
        event_name TEXT,
        event_description TEXT,
        event_count INTEGER
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS zayavka(
    zayavka_id INTEGER PRIMARY KEY,
    full_name TEXT,
    date_age INTEGER,
    rider_exp TEXT,
    skate TEXT,
    helmet TEXT,
    deffender TEXT,
    parents_name TEXT,
    parents_contact TEXT,
    event_id INTEGER
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS accepted(
    zayavka_id INTEGER PRIMARY KEY,
    full_name TEXT,
    date_age INTEGER,
    rider_exp TEXT,
    skate TEXT,
    helmet TEXT,
    deffender TEXT,
    parents_name TEXT,
    parents_contact TEXT,
    event_id INTEGER
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS rejected(
    zayavka_id INTEGER PRIMARY KEY,
    full_name TEXT,
    date_age INTEGER,
    rider_exp TEXT,
    skate TEXT,
    helmet TEXT,
    deffender TEXT,
    parents_name TEXT,
    parents_contact TEXT,
    event_id INTEGER,
    reason TEXT
    )""")

    query = "SELECT * FROM zayavka"
    df = pd.read_sql_query(query, db)

    # Запись данных в Excel файл
    df.to_excel('accepted.xlsx', index=False)

    db.commit()
async def insert_user(user_id, username):
    cur.execute("INSERT OR REPLACE INTO users VALUES (?, ?)", (user_id, username))
    db.commit()

async def insert_event(event_photo, event_name, event_description, event_count):
    cur.execute("INSERT OR REPLACE INTO events(event_photo, event_name, event_description, event_count) VALUES (?, ?, ?, ?)", (event_photo, event_name, event_description, event_count))
    db.commit()

async def get_events():
    events = cur.execute("SELECT * FROM events").fetchall()
    return events

async def get_event(event_id):
    event = cur.execute("SELECT * FROM events WHERE event_id = ?", (event_id,)).fetchone()
    return event

async def get_user(user_id):
    user = cur.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchone()
    return user

async def insert_zayavka(full_name, date_age, rider_exp, skate, helmet, deffender, parents_name, parents_contact, event_id):
    cur.execute("INSERT OR REPLACE INTO zayavka(full_name, date_age, rider_exp, skate, helmet, deffender, parents_name, parents_contact, event_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (full_name, date_age, rider_exp, skate, helmet, deffender, parents_name, parents_contact, event_id))
    db.commit()

async def insert_accepted(zayavka_id, full_name, date_age, rider_exp, skate, helmet, deffender, parents_name, parents_contact, event_id):
    cur.execute("INSERT OR REPLACE INTO accepted(zayavka_id, full_name, date_age, rider_exp, skate, helmet, deffender, parents_name, parents_contact, event_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (zayavka_id, full_name, date_age, rider_exp, skate, helmet, deffender, parents_name, parents_contact, event_id))
    db.commit()

async def insert_rejected(zayavka_id, full_name, date_age, rider_exp, skate, helmet, deffender, parents_name, parents_contact, event_id, reason):
    cur.execute("INSERT OR REPLACE INTO rejected(zayavka_id, full_name, date_age, rider_exp, skate, helmet, deffender, parents_name, parents_contact, event_id, reason) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (zayavka_id, full_name, date_age, rider_exp, skate, helmet, deffender, parents_name, parents_contact, event_id, reason))
    db.commit()

async def get_rejects():
    rejects = cur.execute("SELECT * FROM rejected").fetchall()
    return rejects

async def get_reject(reject_id):
    reject = cur.execute("SELECT * FROM rejected WHERE zayavka_id = ?", (reject_id,)).fetchone()
    return reject

async def get_zayavka(zayavka_id):
    zayavka = cur.execute("SELECT * FROM zayavka WHERE zayavka_id = ?", (zayavka_id,)).fetchone()
    return zayavka

async def get_accept(zayavka_id):
    accept = cur.execute("SELECT * FROM accepted WHERE zayavka_id = ?", (zayavka_id,)).fetchone()
    return accept




async def edit_event_name(event_id, event_name):
    cur.execute("UPDATE events SET event_name = ? WHERE event_id = ?", (event_name, event_id))
    db.commit()

async def edit_event_desc(event_id, event_desc):
    cur.execute("UPDATE events SET event_description = ? WHERE event_id = ?", (event_desc, event_id))
    db.commit()

async def delete_event(event_id: int) -> None:
    cur.execute("DELETE FROM events WHERE event_id = ?", (event_id,))
    db.commit()

async def delete_zayavka_all(event_id):
    cur.execute("DELETE FROM accepted WHERE event_id = ?", (event_id,))
    db.commit()

async def delete_zayavka(event_id):
    cur.execute("DELETE FROM zayavka WHERE event_id = ?", (event_id,))
    db.commit()

async def edit_event_photo(event_id, event_photo):
    cur.execute("UPDATE events SET event_photo = ? WHERE event_id = ?", (event_photo, event_id))
    db.commit()

async def edit_event_count(event_id, event_count):
    cur.execute("UPDATE events SET event_count = ? WHERE event_id = ?", (event_count, event_id))
    db.commit()

async def get_accepted_count(event_id):
    count = cur.execute("SELECT COUNT(*) FROM accepted WHERE event_id = ?", (event_id,)).fetchone()[0]
    return count



