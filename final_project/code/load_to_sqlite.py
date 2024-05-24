import sqlite3
import json

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('pypi_projects.db')
cursor = conn.cursor()

# Create tables
cursor.execute('''
CREATE TABLE IF NOT EXISTS projects (
    project_name TEXT PRIMARY KEY
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS maintainers (
    project_name TEXT,
    maintainer TEXT,
    FOREIGN KEY (project_name) REFERENCES projects (project_name)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS languages (
    project_name TEXT,
    language TEXT,
    FOREIGN KEY (project_name) REFERENCES projects (project_name)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS topics (
    project_name TEXT,
    topic TEXT,
    FOREIGN KEY (project_name) REFERENCES projects (project_name)
)
''')

# Read data from JSON file
with open('pypi_project_info.json', 'r') as file:
    data = json.load(file)

# Insert data into tables
for project_name, details in data.items():
    # Insert into projects table
    cursor.execute('''
    INSERT OR IGNORE INTO projects (project_name)
    VALUES (?)
    ''', (project_name,))

    # Insert into maintainers table
    maintainers = details.get('maintainers', [])
    for maintainer in maintainers:
        cursor.execute('''
        INSERT INTO maintainers (project_name, maintainer)
        VALUES (?, ?)
        ''', (project_name, maintainer))
    
    # Insert into languages table
    languages = details.get('languages', [])
    for language in languages:
        cursor.execute('''
        INSERT INTO languages (project_name, language)
        VALUES (?, ?)
        ''', (project_name, language))
    
    # Insert into topics table
    topics = details.get('topics', [])
    for topic in topics:
        cursor.execute('''
        INSERT INTO topics (project_name, topic)
        VALUES (?, ?)
        ''', (project_name, topic))

# Commit the transaction
conn.commit()

# Close the connection
conn.close()
