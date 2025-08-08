"""
Image encryption module using chaotic maps.
"""

import cv2
import numpy as np
from typing import Tuple, Dict, Any, Optional
from pathlib import Path
import json
import os

from ..utils import (
    ensure_directory_exists,
    get_unique_filename,
    is_valid_image_file,
    write_json_file
)
from . import generate_chaotic_matrix

class ImageEncryptor:
    """
    Class for encrypting images using chaotic maps.
    """
    
    def __init__(self, output_dir: str = "encrypted"):
        """
        Initialize the ImageEncryptor.
        
        Args:
            output_dir: Directory to save encrypted images and metadata
        """
        self.output_dir = Path(output_dir)
        ensure_directory_exists(self.output_dir)
    
    def encrypt_region(self, region: np.ndarray, chaotic_region: np.ndarray) -> np.ndarray:
        """
        Encrypt a region of an image using the chaotic region.
        
        Args:
            region: Image region to encrypt (H x W x C)
            chaotic_region: Chaotic values (H x W)
            
        Returns:
            Encrypted image region
        """
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
        
        # Perform bitwise XOR operation
        encrypted_region = cv2.bitwise_xor(region, chaotic_region)
        
        return encrypted_region
    
    def process_image(
        self,
        image_path: str,
        user_hash: str,
        otp: str,
        output_dir: Optional[str] = None,
        save_metadata: bool = True
    ) -> Dict[str, Any]:
        """
        Process and encrypt an image.
        
        Args:
            image_path: Path to the input image
            user_hash: User's password hash
            otp: One-time password
            output_dir: Directory to save the output (overrides self.output_dir if provided)
            save_metadata: Whether to save encryption metadata
            
        Returns:
            Dictionary containing encryption results and metadata
        """
        # Set output directory
        output_dir = Path(output_dir) if output_dir else self.output_dir
        ensure_directory_exists(output_dir)
        
        # Generate combined hash for encryption
        from ..utils.security import generate_combined_hash
        combined_hash = generate_combined_hash(user_hash, otp)
        
        # Read the image
        if not is_valid_image_file(image_path):
            raise ValueError(f"Invalid image file: {image_path}")
        
        image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
        if image is None:
            raise IOError(f"Failed to read image: {image_path}")
        
        # Generate chaotic matrix using the combined hash as seed
        seed = float.fromhex(combined_hash[:16]) / float(1 << 64)
        chaotic_matrix = generate_chaotic_matrix(image.shape[0], image.shape[1], seed)
        
        # Encrypt the image
        encrypted_image = self.encrypt_region(image, chaotic_matrix)
        
        # Save the encrypted image
        input_path = Path(image_path)
        output_path = get_unique_filename(
            output_dir,
            f"{input_path.stem}_encrypted",
            input_path.suffix.lstrip('.')
        )
        
        cv2.imwrite(str(output_path), encrypted_image)
        
        # Prepare metadata
        metadata = {
            'original_filename': input_path.name,
            'encrypted_filename': output_path.name,
            'image_dimensions': {
                'height': int(image.shape[0]),
                'width': int(image.shape[1]),
                'channels': 1 if len(image.shape) == 2 else image.shape[2]
            },
            'encryption': {
                'algorithm': 'chaotic_maps',
                'user_hash': user_hash,
                'otp': otp,
                'combined_hash': combined_hash,
                'seed': seed
            },
            'timestamp': str(os.path.getmtime(image_path))
        }
        
        # Save metadata if requested
        if save_metadata:
            metadata_path = output_path.with_suffix('.json')
            write_json_file(metadata, metadata_path)
        
        return {
            'success': True,
            'encrypted_path': str(output_path),
            'metadata_path': str(metadata_path) if save_metadata else None,
            'metadata': metadata
        }
