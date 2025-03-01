import os
import json
import logging
import glob
import time
import subprocess

logger = logging.getLogger(__name__)

def force_icloud_download(path, debug=False, max_attempts=3):
    """
    Forces iCloud to download a file using brctl with multiple attempts
    and verification of actual content
    """
    for attempt in range(max_attempts):
        try:
            # First try to evict the file to ensure we get a fresh download
            evict_cmd = ["brctl", "evict", path]
            subprocess.run(evict_cmd, capture_output=True, text=True, timeout=30)
            
            # Force download
            download_cmd = ["brctl", "download", path]
            subprocess.run(download_cmd, capture_output=True, text=True, timeout=30)
            
            # Wait longer for download to complete
            time.sleep(3)
            
            # Verify file exists and has size
            if not os.path.exists(path):
                continue
                
            # Try to read a small bit of content to verify it's actually downloaded
            with open(path, 'r', encoding='utf-8') as f:
                # Read first line or 100 chars to verify content
                content = f.read(100)
                if content:  # If we got actual content
                    if debug:
                        logger.debug(f"Successfully downloaded and verified content for: {path}")
                    return True
                    
            if debug:
                logger.debug(f"Attempt {attempt + 1}: File exists but no content yet")
                
        except Exception as e:
            if debug:
                logger.debug(f"Download attempt {attempt + 1} failed for {path}: {str(e)}")
                
        # Wait longer between attempts
        time.sleep(3)
    
    return False

def read_markdown_files(directory, debug=False):
    """
    Recursively reads all .md files in the specified directory and its subdirectories,
    returning two lists:
    - file_names: list of file names (str)
    - documents: corresponding text contents (str)
    """
    file_names = []
    documents = []
    
    logger.info(f"Reading markdown files from: {directory}")
    
    if not os.path.exists(directory):
        logger.error(f"Directory does not exist: {directory}")
        return file_names, documents
        
    # First, try to force download the entire directory and its contents
    logger.info("Forcing download of directory and contents...")
    try:
        # First evict the directory
        subprocess.run(["brctl", "evict", directory], capture_output=True, text=True, timeout=30)
        # Then download
        subprocess.run(["brctl", "download", directory], capture_output=True, text=True, timeout=30)
        time.sleep(5)  # Give more time for initial downloads
    except Exception as e:
        logger.warning(f"Error forcing directory download: {str(e)}")
        
    for root, dirs, files in os.walk(directory):
        if debug:
            logger.debug(f"Scanning: {root}")
            logger.debug(f"Found files: {files}")
        
        for filename in files:
            if not filename.endswith('.md'):
                continue
                
            path = os.path.join(root, filename)
            if debug:
                logger.debug(f"Processing: {filename}")
            
            # Force download the file first
            if not force_icloud_download(path, debug):
                logger.warning(f"Could not download: {filename}")
                continue
                
            try:
                # Read the file
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                    
                # Skip if content is empty after basic whitespace stripping
                if not content.strip():
                    if debug:
                        logger.debug(f"Skipping empty content: {filename}")
                    continue
                    
                # Store relative path from the base directory
                rel_path = os.path.relpath(path, directory)
                logger.info(f"Adding: {rel_path} ({len(content)} chars)")
                file_names.append(rel_path)
                documents.append(content)
                
            except Exception as e:
                if debug:
                    logger.warning(f"Error reading file: {str(e)}")
                continue
    
    logger.info(f"Found {len(file_names)} markdown files with content")
    return file_names, documents

def save_json(data, output_file):
    """
    Saves a Python dict or list to a JSON file with indentation.
    """
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
