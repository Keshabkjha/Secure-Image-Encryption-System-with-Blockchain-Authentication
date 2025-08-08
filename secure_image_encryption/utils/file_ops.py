"""
File operation utilities for the image encryption system.
"""

import os
import json
from pathlib import Path
from typing import Any, Dict, Optional, Union

def ensure_directory_exists(path: Union[str, Path]) -> None:
    """
    Ensure that the directory exists, creating it if necessary.
    
    Args:
        path: Path to the directory
    """
    path = Path(path) if isinstance(path, str) else path
    path.mkdir(parents=True, exist_ok=True)

def read_json_file(file_path: Union[str, Path]) -> Dict[str, Any]:
    """
    Read a JSON file and return its contents as a dictionary.
    
    Args:
        file_path: Path to the JSON file
        
    Returns:
        Dictionary containing the JSON data
        
    Raises:
        FileNotFoundError: If the file doesn't exist
        json.JSONDecodeError: If the file contains invalid JSON
    """
    file_path = Path(file_path) if isinstance(file_path, str) else file_path
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def write_json_file(
    data: Dict[str, Any], 
    file_path: Union[str, Path],
    indent: int = 2,
    ensure_ascii: bool = False
) -> None:
    """
    Write a dictionary to a JSON file.
    
    Args:
        data: Dictionary to write
        file_path: Path to the output file
        indent: Indentation level for pretty-printing
        ensure_ascii: If True, escape non-ASCII characters
    """
    file_path = Path(file_path) if isinstance(file_path, str) else file_path
    file_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=indent, ensure_ascii=ensure_ascii)

def is_valid_image_file(file_path: Union[str, Path]) -> bool:
    """
    Check if a file is a valid image file based on its extension.
    
    Args:
        file_path: Path to the file
        
    Returns:
        True if the file has a valid image extension, False otherwise
    """
    valid_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp'}
    file_path = Path(file_path) if isinstance(file_path, str) else file_path
    return file_path.suffix.lower() in valid_extensions

def get_unique_filename(directory: Union[str, Path], base_name: str, extension: str) -> Path:
    """
    Generate a unique filename in the specified directory.
    
    Args:
        directory: Directory where the file will be saved
        base_name: Base name for the file (without extension)
        extension: File extension (with or without dot)
        
    Returns:
        Path object with a unique filename
    """
    directory = Path(directory) if isinstance(directory, str) else directory
    extension = f".{extension.lstrip('.')}"  # Ensure extension starts with a dot
    
    counter = 1
    while True:
        if counter == 1:
            filename = f"{base_name}{extension}"
        else:
            filename = f"{base_name}_{counter}{extension}"
            
        file_path = directory / filename
        if not file_path.exists():
            return file_path
            
        counter += 1
