import requests
from bs4 import BeautifulSoup
import json
import time
from tqdm import tqdm
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

def get_project_info(project):
    url = f'https://pypi.org/project/{project}/'
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        maintainers = {span.text.strip() for span in soup.find_all(class_='sidebar-section__user-gravatar-text')}
        
        languages = {a.text.strip() for a in soup.select('strong:contains("Programming Language") + ul > li > a')}
        
        topics = {a.text.strip() for a in soup.select('strong:contains("Topic") + ul > li > a')}
        
        return project, list(maintainers), list(languages), list(topics)
    else:
        print(f"Failed to retrieve data for project {project}: {response.status_code}")
        return project, [], [], []

def read_projects_from_json(filename):
    with open(filename, 'r') as json_file:
        projects = json.load(json_file)
    return projects

def save_project_info_chunk(chunk_data, filename):
    if os.path.exists(filename):
        with open(filename, 'r') as json_file:
            projects_data = json.load(json_file)
    else:
        projects_data = {}

    for project, maintainers, languages, topics in chunk_data:
        projects_data[project] = {
            'maintainers': maintainers,
            'languages': languages,
            'topics': topics
        }

    with open(filename, 'w') as json_file:
        json.dump(projects_data, json_file, indent=4)

def read_existing_project_info(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as json_file:
            project_info = json.load(json_file)
        return set(project_info.keys())
    return set()

def process_chunk(projects_to_fetch, output_filename, threads):
    chunk_data = []
    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = {executor.submit(get_project_info, project): project for project in projects_to_fetch}
        
        for future in tqdm(as_completed(futures), total=len(futures), desc="Processing chunk"):
            project_info = future.result()
            chunk_data.append(project_info)
    
    save_project_info_chunk(chunk_data, output_filename)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Fetch PyPI project maintainers, programming languages, and topics.")
    parser.add_argument('--start', type=int, default=0, help="Start index for the project list.")
    parser.add_argument('--end', type=int, default=None, help="End index for the project list.")
    parser.add_argument('--threads', type=int, default=10, help="Number of threads to use for fetching data.")
    parser.add_argument('--chunk_size', type=int, default=32, help="Number of projects to process in each chunk.")
    args = parser.parse_args()

    projects = read_projects_from_json('pypi_projects.json')
    start = args.start
    end = args.end if args.end is not None else len(projects)
    projects_to_process = projects[start:end]
    
    output_filename = f'pypi_project_info.json'
    processed_projects = read_existing_project_info(output_filename)

    projects_to_fetch = [project for project in projects_to_process if project not in processed_projects]

    for i in range(0, len(projects_to_fetch), args.chunk_size):
        chunk = projects_to_fetch[i:i + args.chunk_size]
        process_chunk(chunk, output_filename, args.threads)
        print(f"Processed chunk {i // args.chunk_size + 1}/{(len(projects_to_fetch) + args.chunk_size - 1) // args.chunk_size}")
