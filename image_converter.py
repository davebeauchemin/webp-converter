#!/usr/bin/env python3
"""
Image to WebP Converter
A micro-app that converts JPG and PNG images to WebP format.
"""

import os
import argparse
import sys
from pathlib import Path
from typing import List, Optional
try:
    from PIL import Image
except ImportError:
    print("Error: Pillow library is required. Install it with: pip install Pillow")
    sys.exit(1)


class ImageConverter:
    """Handles conversion of images to WebP format."""
    
    SUPPORTED_FORMATS = {'.jpg', '.jpeg', '.png'}
    
    def __init__(self, input_folder: str, output_folder: Optional[str] = None, quality: int = 80):
        """
        Initialize the converter.
        
        Args:
            input_folder: Path to folder containing images
            output_folder: Path to output folder (optional, uses sibling 'webp' folder if None)
            quality: WebP quality (0-100, default 80)
        """
        self.input_folder = Path(input_folder)
        if output_folder:
            self.output_folder = Path(output_folder)
        else:
            # Create sibling 'webp' folder
            self.output_folder = self.input_folder.parent / "webp"
        self.quality = quality
        
        # Validate folders
        if not self.input_folder.exists():
            raise FileNotFoundError(f"Input folder does not exist: {self.input_folder}")
        
        if not self.input_folder.is_dir():
            raise NotADirectoryError(f"Input path is not a directory: {self.input_folder}")
    
    def find_images(self) -> List[Path]:
        """Find all supported image files in the input folder."""
        images = []
        for file_path in self.input_folder.iterdir():
            if file_path.is_file() and file_path.suffix.lower() in self.SUPPORTED_FORMATS:
                images.append(file_path)
        return sorted(images)
    
    def convert_image(self, image_path: Path) -> bool:
        """
        Convert a single image to WebP format.
        
        Args:
            image_path: Path to the image file
            
        Returns:
            True if conversion successful, False otherwise
        """
        try:
            # Create output folder if it doesn't exist
            self.output_folder.mkdir(parents=True, exist_ok=True)
            
            # Open and convert image
            with Image.open(image_path) as img:
                # Handle different image modes
                if img.mode == 'P':
                    # Convert palette-based images to RGBA to preserve transparency
                    img = img.convert('RGBA')
                elif img.mode == 'LA':
                    # Convert grayscale with alpha to RGBA
                    img = img.convert('RGBA')
                elif img.mode == 'RGB':
                    # RGB images are fine as-is
                    pass
                elif img.mode == 'RGBA':
                    # RGBA images (with transparency) should stay as RGBA
                    pass
                else:
                    # Convert other modes to RGB
                    img = img.convert('RGB')
                
                # Generate output filename
                output_filename = image_path.stem + '.webp'
                output_path = self.output_folder / output_filename
                
                # Save as WebP
                img.save(output_path, 'WEBP', quality=self.quality, method=6)
                
                print(f"✓ Converted: {image_path.name} -> {output_filename}")
                return True
                
        except Exception as e:
            print(f"✗ Failed to convert {image_path.name}: {str(e)}")
            return False
    
    def convert_all(self) -> dict:
        """
        Convert all images in the input folder.
        
        Returns:
            Dictionary with conversion statistics
        """
        images = self.find_images()
        
        if not images:
            print(f"No supported image files found in: {self.input_folder}")
            return {'total': 0, 'converted': 0, 'failed': 0}
        
        print(f"Found {len(images)} image(s) to convert...")
        print(f"Input folder: {self.input_folder}")
        print(f"Output folder: {self.output_folder}")
        print(f"Quality: {self.quality}%")
        print("-" * 50)
        
        converted = 0
        failed = 0
        
        for image_path in images:
            if self.convert_image(image_path):
                converted += 1
            else:
                failed += 1
        
        return {
            'total': len(images),
            'converted': converted,
            'failed': failed
        }


def main():
    """Main function with command-line interface."""
    parser = argparse.ArgumentParser(
        description="Convert JPG and PNG images to WebP format",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python image_converter.py /path/to/images
  python image_converter.py /path/to/images -o /path/to/output
  python image_converter.py /path/to/images --quality 90
        """
    )
    
    parser.add_argument(
        'input_folder',
        help='Path to folder containing images to convert'
    )
    
    parser.add_argument(
        '-o', '--output',
        help='Output folder (default: sibling "webp" folder)',
        default=None
    )
    
    parser.add_argument(
        '-q', '--quality',
        type=int,
        default=80,
        help='WebP quality (0-100, default: 80)'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='Image Converter 1.0'
    )
    
    args = parser.parse_args()
    
    # Validate quality
    if not 0 <= args.quality <= 100:
        print("Error: Quality must be between 0 and 100")
        sys.exit(1)
    
    try:
        # Create converter and run conversion
        converter = ImageConverter(args.input_folder, args.output, args.quality)
        stats = converter.convert_all()
        
        # Print results
        print("-" * 50)
        print(f"Conversion complete!")
        print(f"Total files: {stats['total']}")
        print(f"Successfully converted: {stats['converted']}")
        print(f"Failed: {stats['failed']}")
        
        if stats['failed'] > 0:
            sys.exit(1)
            
    except (FileNotFoundError, NotADirectoryError) as e:
        print(f"Error: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nConversion cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 