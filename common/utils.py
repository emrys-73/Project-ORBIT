import os
import json

def read_markdown_files(directory):
    """
    Reads all .md files in the specified directory, returning two lists:
    - file_names: list of file names (str)
    - documents: corresponding text contents (str)
    """
    file_names = []
    documents = []
    for filename in os.listdir(directory):
        if filename.endswith(".md"):
            path = os.path.join(directory, filename)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if content:
                    file_names.append(filename)
                    documents.append(content)
    return file_names, documents

def save_json(data, output_file):
    """
    Saves a Python dict or list to a JSON file with indentation.
    """
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
