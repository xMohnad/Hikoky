import json
import os
import urllib.parse
import re

json_file_manga = 'hikoky/scrapers/urls/data/links-manga.json'
chapter_link_file = 'hikoky/scrapers/urls/data/chapter_links.json'
latest_chapters_file = 'hikoky/scrapers/urls/data/latest_chapters.json'
chapter_data = 'hikoky/scrapers/urls/data/chapter_data.json'

def read_json_file(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            return json.load(f)
    return {}

def write_json_file(file_path, data):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def create_path_from_name(name):
    name = re.sub(r'[^\w\s-]', '', name, flags=re.UNICODE)
    name = name.replace(" ", "-").replace("_", "-")
    name = ''.join([char.lower() if 'A' <= char <= 'Z' else char for char in name])
    return name
    
def add_link(file_path, name, value, source):
    path = create_path_from_name(name)
    data = read_json_file(file_path)
    
    if source not in data:
        data[source] = {}
    data[source][path] = value

    write_json_file(file_path, data)
    return path

def get_link(file_path, path, source, key=None):
    data = read_json_file(file_path)
    if source in data and path in data[source]:
        if key:
            return data[source][path].get(key)
        return data[source][path]
    return None

# Functions specific to manga linksض
def add_link_manga(name, url, source):
    return add_link(json_file_manga, name, url, source)

def get_link_manga(path, source):
    return get_link(json_file_manga, path, source)


# Functions specific to chapter links
def add_chapter_link(manga_name, chapter_number, chapter_url, source):
    path = create_path_from_name(manga_name)
    data = read_json_file(chapter_link_file)
    
    if source not in data:
        data[source] = {}
    if path not in data[source]:
        data[source][path] = {}
    
    data[source][path][chapter_number] = chapter_url
    write_json_file(chapter_link_file, data)
    return chapter_number
    
def get_chapter_link(path, chapter_number, source):
    chapter_url = get_link(chapter_link_file, path, source, chapter_number)
    if chapter_url:
        return chapter_url
    return get_latest_chapters(path, chapter_number, source)

# Functions specific to latest chapters

def add_latest_chapters(manga_name, chapter_number, chapter_url, source):
    path = create_path_from_name(manga_name)
    data = read_json_file(latest_chapters_file)
    
    if source not in data:
        data[source] = {}
    if path not in data[source]:
        data[source][path] = {}
    
    data[source][path][chapter_number] = chapter_url
    write_json_file(latest_chapters_file, data)
    return chapter_number
    
def get_latest_chapters(path, chapter_number, source):
    return get_link(latest_chapters_file, path, source, chapter_number)


def load_chapter(url, source):
    """Load data from a JSON file if it exists."""
    if os.path.exists(chapter_data):
        with open(chapter_data , 'r', encoding='utf-8') as file:
            data = json.load(file)
            if source in data and url in data[source]:
                return data[source][url]
    return {}

def save_chapter(data, url, source):
    if data["next_chapter_link"] is not None:
        """Save data to a JSON file."""
        # Load existing data if file exists
        existing_data = read_json_file(chapter_data)
        
        # Create or update the source data
        if source not in existing_data:
            existing_data[source] = {}
        existing_data[source][url] = data
        
        # Write the updated data to the JSON file
        write_json_file(chapter_data, existing_data)
