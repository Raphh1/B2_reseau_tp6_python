import requests
import os
import sys

def get_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as err:
        print(f"Error getting content from {url}: {err}")
        sys.exit(1)

def write_content(content, file_path):
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"Content written to {file_path}")
    except IOError as e:
        print(f"Error writing to {file_path}: {e}")
        sys.exit(1)

def main():
    if len(sys.argv) != 2:
        print("Usage: python web_sync_multiple.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]

    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        sys.exit(1)

    with open(file_path, 'r') as file:
        urls = [line.strip() for line in file]

    for url in urls:
        content = get_content(url)
        filename = f'/tmp/web_{url.replace("https://", "").replace("/", "_")}'
        write_content(content, filename)

if __name__ == "__main__":
    main()
