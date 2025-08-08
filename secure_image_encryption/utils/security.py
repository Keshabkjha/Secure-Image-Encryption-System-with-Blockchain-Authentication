"""
Security-related utilities for the image encryption system.
"""

import hashlib
import os
import random
import string
from typing import Tuple

def hash_string(s: str) -> str:
    """
    Hash a string using SHA-256.
    
    Args:
        s: String to hash
        
    Returns:
        Hex digest of the hashed string
    """
    return hashlib.sha256(s.encode()).hexdigest()

def generate_otp(length: int = 6) -> str:
    """
    Generate a random OTP (One-Time Password).
    
    Args:
        length: Length of the OTP
        
    Returns:
        Random OTP string
    """
    digits = string.digits
    return ''.join(random.choice(digits) for _ in range(length))

def generate_combined_hash(user_hash: str, otp_hash: str) -> str:
    """
    Combine two hashes and hash the result.
    
    Args:
        user_hash: First hash (user password hash)
        otp_hash: Second hash (OTP hash)
        
    Returns:
        Combined hash
    """
    combined = f"{user_hash}:{otp_hash}"
    return hash_string(combined)

def generate_secure_seed(user_input: str, salt: bytes = None) -> Tuple[bytes, bytes]:
    """
    Generate a secure seed for cryptographic operations.
    
    Args:
        user_input: User-provided input (e.g., password)
        salt: Optional salt (if None, a new one will be generated)
        
    Returns:
        Tuple of (derived_key, salt)
    """
    if salt is None:
        salt = os.urandom(16)
    
    # Use PBKDF2 for key derivation
    dk = hashlib.pbkdf2_hmac(
        'sha256',
        user_input.encode('utf-8'),
        salt,
        100000  # Number of iterations
    )
    
    return dk, salt
