import requests
import os
import sys

def get_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  
        return response.text
    except requests.exceptions.RequestException as err:
        print(f"Error getting content from {url}: {err}")
        sys.exit(1)

def write_content(content, file_path):
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)  
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"Content written to {file_path}")
    except IOError as e:
        print(f"Error writing to {file_path}: {e}")
        sys.exit(1)

def main():
    if len(sys.argv) != 2:
        print("Usage: python web_sync.py <url>")
        sys.exit(1)

    url = sys.argv[1]
    content = get_content(url)

    file_path = '/tmp/web_page.html'
    write_content(content, file_path)

if __name__ == "__main__":
    main()
