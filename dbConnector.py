import sqlite3;

def init_db():
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS house_codes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        address TEXT NOT NULL,
        house_number TEXT NOT NULL,
        code TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

def add_address(address, house_number, code):
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO house_codes (address, house_number, code) VALUES (?, ?, ?)', (address, house_number, code))
    conn.commit()
    conn.close()

def get_code(address):
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT house_number, code FROM house_codes WHERE address = ?', (address,))
    result = cursor.fetchall()
    conn.close()
    return result

def update_code(address, house_number, code):
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE house_codes SET code = ? WHERE address = ? AND house_number = ?', (code, address, house_number))
    conn.commit()
    conn.close()