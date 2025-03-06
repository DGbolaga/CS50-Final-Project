import sqlite3

conn = sqlite3.connect('books.db')
cursor = conn.cursor()

# Create users table first
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    password TEXT NOT NULL,
    email TEXT NOT NULL,
    UNIQUE(email)
)
''')

# Create books table with added user reference
cursor.execute('''
CREATE TABLE IF NOT EXISTS books (
    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    authors TEXT NOT NULL,
    description TEXT NOT NULL,
    category TEXT NOT NULL,
    cover_img TEXT NOT NULL,
    location TEXT NOT NULL,
    book_format TEXT NOT NULL,
    ratings TEXT NOT NULL,
    added_by INTEGER NOT NULL,
    FOREIGN KEY (added_by) REFERENCES users(user_id)
)
''')

conn.commit()
conn.close()

print('Database and table successfully created')
