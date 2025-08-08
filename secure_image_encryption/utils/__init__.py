"""
Utility functions for the secure image encryption system.

This module contains various utility functions for security, file operations,
and other helper functions used throughout the application.
"""

try:
    from .security import (
        hash_string,
        generate_otp,
        generate_combined_hash,
        generate_secure_seed
    )
    from .file_ops import (
        ensure_directory_exists,
        read_json_file,
        write_json_file,
        is_valid_image_file,
        get_unique_filename
    )
    
    __all__ = [
        # Security functions
        'hash_string',
        'generate_otp',
        'generate_combined_hash',
        'generate_secure_seed',
        
        # File operations
        'ensure_directory_exists',
        'read_json_file',
        'write_json_file',
        'is_valid_image_file',
        'get_unique_filename',
    ]
    
except ImportError as e:
    print(f"Warning: Could not import utility modules: {e}")
    __all__ = []
