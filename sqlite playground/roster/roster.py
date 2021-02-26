import json
import sqlite3

conn = sqlite3.connect('rosterdb.sqlite')
cur = conn.cursor()

# Automatic Incrementing ID column
cur.executescript('''
DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Member;
DROP TABLE IF EXISTS Course;


CREATE TABLE User (
    id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name   TEXT UNIQUE
);

CREATE TABLE Course (
    id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    title  TEXT UNIQUE
);

CREATE TABLE Member (
    user_id     INTEGER,
    course_id   INTEGER,
    role       INTEGER,
    PRIMARY KEY (user_id, course_id)
)
''')

fname = input('Enter file name: ')
if len(fname) < 1:
    fname = 'roster_data.json'



str_data = open(fname).read()
json_data = json.loads(str_data)

for entry in json_data:

    name = entry[0];
    title = entry[1];
    role = entry[2];
    print((name, title, role))

    # OR IGNORE avoiding code to fail if Duplicate values inserted
    # Inserting to name column in User table String at pos 0 from JSON
    cur.execute('''INSERT OR IGNORE INTO User (name)
        VALUES ( ? )''', ( name, ) )
    cur.execute('SELECT id FROM User WHERE name = ? ', (name, ))
    user_id = cur.fetchone()[0]

    # Inserting to title column in Course table String at pos 1 from JSON
    cur.execute('''INSERT OR IGNORE INTO Course (title)
        VALUES ( ? )''', ( title, ) )
    cur.execute('SELECT id FROM Course WHERE title = ? ', (title, ))
    course_id = cur.fetchone()[0]

    # Inserting to title column in Member table String at pos 1 from JSON
    cur.execute('''INSERT OR REPLACE INTO Member
        (user_id, course_id, role ) VALUES ( ?, ?, ? ) ''',
        ( user_id, course_id, role ) )
    cur.execute('SELECT role FROM (Member JOIN User JOIN Course ON Member.user_id = User.id AND Member.course_id = Course.id) WHERE role = ? ', (role, ))
    role = cur.fetchone()[0]
    conn.commit()