import sqlite3
import json

# Connect to the SQLite database
conn = sqlite3.connect('pypi_projects.db')
cursor = conn.cursor()

# List of top-level topics to search for
topics = [
    "Software Development",
    "Scientific/Engineering",
    "Internet",
    "System",
    "Text Processing",
    "Multimedia",
    "Communications",
    "Office/Business",
    "Database",
    "Security",
    "Games/Entertainment"
]

# List of specified languages to search for
languages_of_interest = ["C", "C++", "Cython", "JavaScript", "SQL", "Fortran", "Rust", "Unix Shell"]

# Function to extract the top-level category from a hierarchical string
def get_top_level_category(full_string):
    return full_string.split(' ::')[0]

# Function to find project counts for specified languages for a given topic
def find_language_counts_for_topic(topic):
    query = '''
    SELECT languages.language, COUNT(DISTINCT projects.project_name) as project_count
    FROM projects
    JOIN topics ON projects.project_name = topics.project_name
    JOIN languages ON projects.project_name = languages.project_name
    WHERE topics.topic LIKE ?
    GROUP BY languages.language
    '''
    cursor.execute(query, (f'%{topic}%',))
    raw_results = cursor.fetchall()

    # Parse languages to top-level categories and filter by specified languages
    parsed_results = {language: 0 for language in languages_of_interest}
    for row in raw_results:
        top_level_language = get_top_level_category(row[0])
        if top_level_language in parsed_results:
            parsed_results[top_level_language] += row[1]

    return parsed_results

# Dictionary to store the results
results_dict = {}

# Iterate through each topic and store the project counts for specified languages
for topic in topics:
    results_dict[topic] = find_language_counts_for_topic(topic)

# Save the results to a JSON file
with open('language_counts_by_topic.json', 'w') as json_file:
    json.dump(results_dict, json_file, indent=4)

# Close the connection
conn.close()
