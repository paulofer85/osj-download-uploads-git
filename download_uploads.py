#!/usr/bin/env python3
import os
import requests
from urllib.parse import urljoin, urlparse
from pathlib import Path
import json

def download_uploads():
    base_url = "https://proxy-osj-analizer-354c97976fe8.herokuapp.com"
    uploads_url = f"{base_url}/uploads"
    
    # Crear directorio local para descargar
    download_dir = Path("downloads")
    download_dir.mkdir(exist_ok=True)
    
    print(f"Descargando archivos de: {uploads_url}")
    
    try:
        # Primero, intentar obtener la lista de archivos
        list_url = f"{base_url}/api/list_files"
        print(f"Obteniendo lista de archivos desde: {list_url}")
        
        response = requests.get(list_url)
        if response.status_code == 200:
            files = response.json()
            print(f"Encontrados {len(files)} archivos")
            
            for file_info in files:
                filename = file_info['name']
                file_url = file_info['url']
                file_path = download_dir / filename
                
                print(f"Descargando: {filename}")
                
                # Descargar el archivo
                file_response = requests.get(file_url)
                if file_response.status_code == 200:
                    with open(file_path, 'wb') as f:
                        f.write(file_response.content)
                    print(f"  ✓ Descargado: {filename}")
                    
                    # También descargar el archivo de metadatos si existe
                    metadata_url = f"{file_url}.json"
                    metadata_response = requests.get(metadata_url)
                    if metadata_response.status_code == 200:
                        metadata_path = download_dir / f"{filename}.json"
                        with open(metadata_path, 'w', encoding='utf-8') as f:
                            json.dump(metadata_response.json(), f, indent=2, ensure_ascii=False)
                        print(f"  ✓ Metadatos descargados: {filename}.json")
                else:
                    print(f"  ✗ Error descargando: {filename}")
        else:
            print(f"Error obteniendo lista de archivos: {response.status_code}")
            
    except Exception as e:
        print(f"Error: {e}")
        print("Intentando descargar archivos conocidos...")
        
        # Lista de archivos conocidos (puedes agregar más)
        known_files = [
            # Agrega aquí los nombres de archivos que sabes que existen
            # "2024-07-28_foto_abc123.jpg",
            # "2024-07-28_foto_abc123.jpg.json",
        ]
        
        for filename in known_files:
            file_url = f"{uploads_url}/{filename}"
            file_path = download_dir / filename
            
            print(f"Descargando: {filename}")
            try:
                response = requests.get(file_url)
                if response.status_code == 200:
                    with open(file_path, 'wb') as f:
                        f.write(response.content)
                    print(f"  ✓ Descargado: {filename}")
                else:
                    print(f"  ✗ No encontrado: {filename}")
            except Exception as e:
                print(f"  ✗ Error: {filename} - {e}")
    
    print(f"\nDescarga completada. Archivos guardados en: {download_dir.absolute()}")

if __name__ == "__main__":
    download_uploads() 