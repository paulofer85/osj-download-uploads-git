#!/usr/bin/env python3
import os
import requests
from urllib.parse import urljoin, urlparse
from pathlib import Path
import json

def download_uploads():
    base_url = "https://proxy-osj-analizer-354c97976fe8.herokuapp.com"
    uploads_url = f"{base_url}/uploads"
    
    # Create local directory for downloads
    download_dir = Path("downloads")
    download_dir.mkdir(exist_ok=True)
    
    print(f"Downloading files from: {uploads_url}")
    
    try:
        # First, try to get the list of files
        list_url = f"{base_url}/api/list_files"
        print(f"Getting file list from: {list_url}")
        
        response = requests.get(list_url)
        if response.status_code == 200:
            files = response.json()
            print(f"Found {len(files)} files")
            
            for file_info in files:
                filename = file_info['name']
                file_url = file_info['url']
                file_path = download_dir / filename
                
                print(f"Downloading: {filename}")
                
                # Download the file
                file_response = requests.get(file_url)
                if file_response.status_code == 200:
                    with open(file_path, 'wb') as f:
                        f.write(file_response.content)
                    print(f"  ✓ Downloaded: {filename}")
                    
                    # Also download the metadata file if it exists
                    metadata_url = f"{file_url}.json"
                    metadata_response = requests.get(metadata_url)
                    if metadata_response.status_code == 200:
                        metadata_path = download_dir / f"{filename}.json"
                        with open(metadata_path, 'w', encoding='utf-8') as f:
                            json.dump(metadata_response.json(), f, indent=2, ensure_ascii=False)
                        print(f"  ✓ Metadata downloaded: {filename}.json")
                else:
                    print(f"  ✗ Error downloading: {filename}")
        else:
            print(f"Error getting file list: {response.status_code}")
            
    except Exception as e:
        print(f"Error: {e}")
        print("Trying to download known files...")
        
        # List of known files (you can add more)
        known_files = [
            # Add here the filenames you know exist
            # "2024-07-28_foto_abc123.jpg",
            # "2024-07-28_foto_abc123.jpg.json",
        ]
        
        for filename in known_files:
            file_url = f"{uploads_url}/{filename}"
            file_path = download_dir / filename
            
            print(f"Downloading: {filename}")
            try:
                response = requests.get(file_url)
                if response.status_code == 200:
                    with open(file_path, 'wb') as f:
                        f.write(response.content)
                    print(f"  ✓ Downloaded: {filename}")
                else:
                    print(f"  ✗ Not found: {filename}")
            except Exception as e:
                print(f"  ✗ Error: {filename} - {e}")
    
    print(f"\nDownload completed. Files saved in: {download_dir.absolute()}")

if __name__ == "__main__":
    download_uploads() 