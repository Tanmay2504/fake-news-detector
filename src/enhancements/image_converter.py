"""
Image Format Converter
Converts all image formats (AVIF, WebP, HEIC, etc.) to formats compatible with detection models
"""

from PIL import Image
import pillow_heif
from pathlib import Path
import tempfile
import os
from typing import Optional

# Register HEIF opener
pillow_heif.register_heif_opener()

# Supported formats
SUPPORTED_FORMATS = {
    '.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.tif',
    '.webp', '.avif', '.heic', '.heif', '.svg'
}

def convert_to_compatible_format(image_path: str, output_format: str = 'JPEG') -> str:
    """
    Convert any image format to a compatible format (JPEG/PNG)
    
    Args:
        image_path: Path to input image
        output_format: Output format ('JPEG' or 'PNG')
    
    Returns:
        Path to converted image (or original if already compatible)
    """
    try:
        # Open image with all format support
        img = Image.open(image_path)
        
        # Convert RGBA to RGB if saving as JPEG
        if output_format == 'JPEG' and img.mode in ('RGBA', 'LA', 'P'):
            # Create white background
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
            img = background
        elif img.mode not in ('RGB', 'L'):
            img = img.convert('RGB')
        
        # Get file extension
        ext = Path(image_path).suffix.lower()
        
        # If already compatible format, return original
        if ext in {'.jpg', '.jpeg', '.png'} and img.mode in ('RGB', 'L'):
            return image_path
        
        # Create temporary file with compatible format
        temp_dir = tempfile.gettempdir()
        original_name = Path(image_path).stem
        temp_path = os.path.join(temp_dir, f"{original_name}_converted.{output_format.lower()}")
        
        # Save converted image
        img.save(temp_path, format=output_format, quality=95)
        
        return temp_path
        
    except Exception as e:
        raise Exception(f"Failed to convert image format: {e}")


def is_supported_format(file_path: str) -> bool:
    """Check if file format is supported"""
    ext = Path(file_path).suffix.lower()
    return ext in SUPPORTED_FORMATS


def get_image_info(image_path: str) -> dict:
    """Get detailed information about an image"""
    try:
        img = Image.open(image_path)
        
        return {
            'format': img.format,
            'mode': img.mode,
            'size': img.size,
            'width': img.width,
            'height': img.height,
            'file_size': os.path.getsize(image_path),
            'has_transparency': img.mode in ('RGBA', 'LA', 'P'),
            'is_animated': getattr(img, 'is_animated', False)
        }
    except Exception as e:
        return {'error': str(e)}


def prepare_image_for_detection(image_path: str) -> str:
    """
    Prepare any image format for detection models
    
    Args:
        image_path: Path to input image
        
    Returns:
        Path to processed image (compatible format)
    """
    if not is_supported_format(image_path):
        raise ValueError(f"Unsupported image format: {Path(image_path).suffix}")
    
    # Convert to JPEG for maximum compatibility
    return convert_to_compatible_format(image_path, output_format='JPEG')
