# -*- coding: utf-8 -*-
"""
Created on Sat Nov  2 09:41:16 2019

@author: Familia Cuero
"""
import sqlite3
import json
conn = sqlite3.connect('roster.sqlite')
cur = conn.cursor()
cur.executescript(''' 
DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS Courses; 
DROP TABLE IF EXISTS Member; 

CREATE TABLE Users (
id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
name TEXT UNIQUE
);     

CREATE TABLE Courses (
id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
title TEXT UNIQUE
);   

CREATE TABLE Member (
user_id INTEGER, 
course_id INTEGER, 
role INTEGER,
PRIMARY KEY (user_id, course_id)
);               
''')
str_data = open('roster_data.json').read()
file = json.loads(str_data)
for entry in file:
    name = entry[0]
    title = entry[1]
    role = entry[2]
    
    if name is None or title is None or role is None:
        continue
    
    print(name, title, role)
    
    cur.execute('INSERT OR IGNORE INTO Users (name) VALUES (?)', (name,))
    cur.execute('SELECT id FROM Users WHERE name = ?', (name,))
    user_id = cur.fetchone()[0]
    
    cur.execute('INSERT OR IGNORE INTO Courses (title) VALUES (?)', (title,))
    cur.execute('SELECT id FROM Courses WHERE title = ?', (title,))
    course_id = cur.fetchone()[0]
    
    cur.execute('''INSERT OR REPLACE INTO 
                Member (user_id, course_id, role)
                VALUES (?, ?, ?)
                ''', (user_id, course_id, role))
    conn.commit()
    
sqlstr = '''SELECT Users.name, Member.role, Courses.title 
FROM Users JOIN Member JOIN Courses ON Member.course_id = Courses.id 
AND Member.user_id = Users.id ORDER BY Courses.title, Member.role DESC, Users.name;'''
cur.execute(sqlstr)
#SELECT hex(Users.name || Courses.title || Member.role ) AS X FROM 
#    Users JOIN Member JOIN Courses 
#    ON Users.id = Member.user_id AND Member.course_id = Courses.id
#    ORDER BY X

