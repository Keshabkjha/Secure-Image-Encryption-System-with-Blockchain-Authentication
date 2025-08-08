"""
Image decryption module using chaotic maps.
"""

import cv2
import numpy as np
from typing import Dict, Any, Optional, Tuple
from pathlib import Path
import json
import os

from ..utils import (
    ensure_directory_exists,
    get_unique_filename,
    is_valid_image_file,
    read_json_file
)
from . import generate_chaotic_matrix

class ImageDecryptor:
    """
    Class for decrypting images that were encrypted using chaotic maps.
    """
    
    def __init__(self, output_dir: str = "decrypted"):
        """
        Initialize the ImageDecryptor.
        
        Args:
            output_dir: Directory to save decrypted images
        """
        self.output_dir = Path(output_dir)
        ensure_directory_exists(self.output_dir)
    
    def decrypt_region(self, region: np.ndarray, chaotic_region: np.ndarray) -> np.ndarray:
        """
        Decrypt a region of an image using the chaotic region.
        
        Args:
            region: Encrypted image region (H x W x C)
            chaotic_region: Chaotic values (H x W)
            
        Returns:
            Decrypted image region
        """
        # Decryption is the same as encryption for XOR-based operations
        # Ensure chaotic_region has the same spatial dimensions as the region
        if chaotic_region.shape != region.shape[:2]:
            # Resize chaotic_region to match region dimensions
            chaotic_region = cv2.resize(chaotic_region, 
                                     (region.shape[1], region.shape[0]),
                                     interpolation=cv2.INTER_LINEAR)
        
        # Normalize chaotic values to 0-255
        chaotic_region = (chaotic_region * 255).astype(np.uint8)
        
        # If region is grayscale, add channel dimension
        if len(region.shape) == 2:
            region = np.expand_dims(region, axis=-1)
        
        # Ensure chaotic_region has the same number of channels as region
        if len(chaotic_region.shape) == 2:
            chaotic_region = np.tile(chaotic_region[..., np.newaxis], (1, 1, region.shape[2]))
        
        # Perform bitwise XOR operation (same as encryption)
        decrypted_region = cv2.bitwise_xor(region, chaotic_region)
        
        return decrypted_region
    
    def load_metadata(self, metadata_path: str) -> Dict[str, Any]:
        """
        Load encryption metadata from a JSON file.
        
        Args:
            metadata_path: Path to the metadata JSON file
            
        Returns:
            Dictionary containing the metadata
            
        Raises:
            FileNotFoundError: If the metadata file doesn't exist
            json.JSONDecodeError: If the metadata file is not valid JSON
            KeyError: If required fields are missing
        """
        metadata = read_json_file(metadata_path)
        
        # Validate required fields
        required_fields = [
            'original_filename',
            'encrypted_filename',
            'image_dimensions',
            'encryption'
        ]
        
        for field in required_fields:
            if field not in metadata:
                raise ValueError(f"Missing required field in metadata: {field}")
        
        return metadata
    
    def process_image(
        self,
        encrypted_path: str,
        user_hash: str,
        otp: str,
        metadata_path: Optional[str] = None,
        output_dir: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Process and decrypt an encrypted image.
        
        Args:
            encrypted_path: Path to the encrypted image
            user_hash: User's password hash (must match the one used for encryption)
            otp: One-time password (must match the one used for encryption)
            metadata_path: Optional path to the metadata file
            output_dir: Directory to save the decrypted image
            
        Returns:
            Dictionary containing decryption results and metadata
        """
        # Set output directory
        output_dir = Path(output_dir) if output_dir else self.output_dir
        ensure_directory_exists(output_dir)
        
        # Load metadata if provided
        metadata = None
        if metadata_path:
            try:
                metadata = self.load_metadata(metadata_path)
                # Verify the user_hash and OTP match the ones used for encryption
                if (metadata['encryption']['user_hash'] != user_hash or 
                    metadata['encryption']['otp'] != otp):
                    return {
                        'success': False,
                        'error': 'Invalid credentials',
                        'message': 'User hash or OTP does not match encryption credentials'
                    }
            except Exception as e:
                return {
                    'success': False,
                    'error': 'Invalid metadata',
                    'message': str(e)
                }
        
        # Read the encrypted image
        if not is_valid_image_file(encrypted_path):
            return {
                'success': False,
                'error': 'Invalid file',
                'message': f'Not a valid image file: {encrypted_path}'
            }
        
        try:
            encrypted_image = cv2.imread(encrypted_path, cv2.IMREAD_UNCHANGED)
            if encrypted_image is None:
                raise IOError(f"Failed to read encrypted image: {encrypted_path}")
            
            # Generate the same chaotic matrix used for encryption
            if metadata:
                # Use seed from metadata if available
                seed = metadata['encryption']['seed']
            else:
                # Try to generate the same seed using the user_hash and OTP
                from ..utils.security import generate_combined_hash
                combined_hash = generate_combined_hash(user_hash, otp)
                seed = float.fromhex(combined_hash[:16]) / float(1 << 64)
            
            chaotic_matrix = generate_chaotic_matrix(
                encrypted_image.shape[0], 
                encrypted_image.shape[1], 
                seed
            )
            
            # Decrypt the image
            decrypted_image = self.decrypt_region(encrypted_image, chaotic_matrix)
            
            # Save the decrypted image
            input_path = Path(encrypted_path)
            output_path = get_unique_filename(
                output_dir,
                f"{input_path.stem}_decrypted",
                input_path.suffix.lstrip('.')
            )
            
            cv2.imwrite(str(output_path), decrypted_image)
            
            # Prepare result
            result = {
                'success': True,
                'decrypted_path': str(output_path),
                'original_dimensions': {
                    'height': int(decrypted_image.shape[0]),
                    'width': int(decrypted_image.shape[1]),
                    'channels': 1 if len(decrypted_image.shape) == 2 else decrypted_image.shape[2]
                },
                'metadata': metadata
            }
            
            return result
            
        except Exception as e:
            return {
                'success': False,
                'error': 'Decryption failed',
                'message': str(e)
            }
