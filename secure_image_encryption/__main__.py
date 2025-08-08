"""
Main entry point for the secure image encryption system.

This module provides a command-line interface for encrypting and decrypting images
using chaotic maps and blockchain-based authentication.
"""

import argparse
import os
import sys
from pathlib import Path
from typing import Optional, Dict, Any

from .core.encryption import ImageEncryptor
from .core.decryption import ImageDecryptor
from .utils.security import hash_string, generate_otp
from .utils.file_ops import is_valid_image_file, read_json_file

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Secure Image Encryption System with Blockchain Authentication"
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Encrypt command
    encrypt_parser = subparsers.add_parser('encrypt', help='Encrypt an image')
    encrypt_parser.add_argument('image_path', help='Path to the image to encrypt')
    encrypt_parser.add_argument('--output-dir', default='encrypted', 
                              help='Directory to save encrypted images (default: encrypted)')
    encrypt_parser.add_argument('--password', help='Password for encryption (will prompt if not provided)')
    encrypt_parser.add_argument('--otp', help='One-time password (will generate if not provided)')
    
    # Decrypt command
    decrypt_parser = subparsers.add_parser('decrypt', help='Decrypt an image')
    decrypt_parser.add_argument('image_path', help='Path to the encrypted image')
    decrypt_parser.add_argument('--metadata', help='Path to the metadata JSON file')
    decrypt_parser.add_argument('--output-dir', default='decrypted', 
                              help='Directory to save decrypted images (default: decrypted)')
    decrypt_parser.add_argument('--password', help='Password for decryption (will prompt if not provided)')
    decrypt_parser.add_argument('--otp', help='One-time password (required if not in metadata)')
    
    return parser.parse_args()

def get_password(prompt: str = "Enter password: ") -> str:
    """Safely get password from user input."""
    import getpass
    return getpass.getpass(prompt)

def main():
    """Main entry point for the script."""
    args = parse_arguments()
    
    if args.command == 'encrypt':
        encrypt_image(args)
    elif args.command == 'decrypt':
        decrypt_image(args)
    else:
        print("Please specify a command: encrypt or decrypt")
        sys.exit(1)

def encrypt_image(args):
    """Handle image encryption."""
    # Get password
    password = args.password or get_password()
    user_hash = hash_string(password)
    
    # Generate or use provided OTP
    otp = args.otp or generate_otp()
    print(f"Generated OTP: {otp}")
    print("Please save this OTP as it will be required for decryption.")
    
    # Initialize encryptor
    encryptor = ImageEncryptor(output_dir=args.output_dir)
    
    try:
        # Process the image
        result = encryptor.process_image(
            image_path=args.image_path,
            user_hash=user_hash,
            otp=otp,
            output_dir=args.output_dir,
            save_metadata=True
        )
        
        if result['success']:
            print(f"\n✅ Image successfully encrypted!")
            print(f"   Encrypted image: {result['encrypted_path']}")
            print(f"   Metadata: {result['metadata_path']}")
            print("\n🔑 IMPORTANT: Keep your OTP and password secure!")
            print("   You'll need both to decrypt the image.")
        else:
            print(f"\n❌ Encryption failed: {result.get('message', 'Unknown error')}")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n❌ An error occurred during encryption: {str(e)}")
        sys.exit(1)

def decrypt_image(args):
    """Handle image decryption."""
    # Get password
    password = args.password or get_password()
    user_hash = hash_string(password)
    
    # Get OTP from args or prompt
    otp = args.otp
    if not otp:
        if args.metadata:
            try:
                metadata = read_json_file(args.metadata)
                otp = metadata['encryption']['otp']
            except (FileNotFoundError, KeyError, json.JSONDecodeError):
                otp = input("Enter OTP: ")
        else:
            otp = input("Enter OTP: ")
    
    # Initialize decryptor
    decryptor = ImageDecryptor(output_dir=args.output_dir)
    
    try:
        # Process the image
        result = decryptor.process_image(
            encrypted_path=args.image_path,
            user_hash=user_hash,
            otp=otp,
            metadata_path=args.metadata,
            output_dir=args.output_dir
        )
        
        if result['success']:
            print(f"\n✅ Image successfully decrypted!")
            print(f"   Decrypted image: {result['decrypted_path']}")
        else:
            print(f"\n❌ Decryption failed: {result.get('message', 'Unknown error')}")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n❌ An error occurred during decryption: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
