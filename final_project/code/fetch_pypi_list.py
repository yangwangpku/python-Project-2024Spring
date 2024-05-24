import requests
from bs4 import BeautifulSoup
import json

def get_pypi_projects():
    """
    Fetches the list of all projects from the PyPI simple index.

    Returns:
        List of project names.
    """
    url = 'https://pypi.org/simple/'
    response = requests.get(url)
    
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'lxml')
        # Extract project names from the anchor tags
        projects = [a.text for a in soup.find_all('a')]
        return projects
    else:
        # Raise an exception if the request was not successful
        raise Exception(f"Failed to retrieve data: {response.status_code}")

def save_projects_to_json(filename):
    """
    Saves the list of PyPI projects to a JSON file.

    Args:
        filename (str): The name of the file to save the projects to.
    """
    projects = get_pypi_projects()
    # Write the projects list to a JSON file
    with open(filename, 'w') as json_file:
        json.dump(projects, json_file, indent=4)
    print(f"Saved {len(projects)} projects to {filename}")

if __name__ == "__main__":
    # Save the list of PyPI projects to 'pypi_projects.json'
    save_projects_to_json('pypi_projects.json')
