import sqlite3
import json

# Connect to the SQLite database
conn = sqlite3.connect('pypi_projects.db')
cursor = conn.cursor()

# Step 1: Identify the top 100 maintainers
top_maintainers_query = '''
SELECT maintainer, COUNT(project_name) as project_count
FROM maintainers
GROUP BY maintainer
ORDER BY project_count DESC
LIMIT 50
'''

cursor.execute(top_maintainers_query)
top_maintainers = cursor.fetchall()

# Step 2: Find the number of projects each pair of top maintainers cooperate on
cooperation_query = '''
SELECT m1.maintainer AS maintainer1, m2.maintainer AS maintainer2, COUNT(*) AS project_count
FROM maintainers m1
JOIN maintainers m2 ON m1.project_name = m2.project_name
WHERE m1.maintainer < m2.maintainer
AND m1.maintainer IN ({placeholders})
AND m2.maintainer IN ({placeholders})
GROUP BY m1.maintainer, m2.maintainer
ORDER BY project_count DESC
'''

# Generate placeholders for the IN clause
placeholders = ', '.join('?' for _ in top_maintainers)

# Extract only the maintainer names for placeholders
top_maintainer_names = [row[0] for row in top_maintainers]

# Execute the cooperation query
cursor.execute(cooperation_query.format(placeholders=placeholders), top_maintainer_names * 2)
cooperation_results = cursor.fetchall()

# Prepare the cooperation data for JSON serialization
cooperation_data = [
    {"maintainer1": row[0], "maintainer2": row[1], "project_count": row[2]}
    for row in cooperation_results
]

# Prepare the project count data for JSON serialization
project_count_data = [
    {"maintainer": row[0], "project_count": row[1]}
    for row in top_maintainers
]

# Combine the results into a single dictionary
combined_data = {
    "cooperation": cooperation_data,
    "project_counts": project_count_data
}

# Save the results to a JSON file
with open('maintainers_cooperation.json', 'w') as json_file:
    json.dump(combined_data, json_file, indent=4)

# Close the connection
conn.close()
