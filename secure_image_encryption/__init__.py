"""
Secure Image Encryption System with Blockchain Authentication

This package provides secure image encryption and decryption functionality
using chaotic maps and blockchain technology for authentication.
"""

__version__ = "0.1.0"

# Import key components for easier access
try:
    from secure_image_encryption.core.chaotic_maps import (
        ikeda_map,
        circle_map,
        logistic_map,
        generate_chaotic_matrix
    )
    from secure_image_encryption.utils.security import (
        hash_string,
        generate_otp,
        generate_combined_hash,
        generate_secure_seed
    )
    
    __all__ = [
        'ikeda_map',
        'circle_map',
        'logistic_map',
        'generate_chaotic_matrix',
        'hash_string',
        'generate_otp',
        'generate_combined_hash',
        'generate_secure_seed',
    ]
    
except ImportError as e:
    print(f"Warning: Could not import all modules: {e}")
    __all__ = []
