# Image to WebP Converter

A simple micro-app that converts JPG and PNG images to WebP format locally.

## Features

- Converts JPG and PNG images to WebP format
- Supports batch processing of entire folders
- Configurable output quality
- Option to specify output folder or use sibling "webp" folder by default
- Progress indication and error handling
- Handles transparent PNGs properly
- Cross-platform support (Windows, macOS, Linux)

## Requirements

- Python 3.6 or higher
- Pillow library

## Installation

1. Clone or download this repository
2. Install the required dependencies:

**For zsh (macOS default) and most systems:**
```zsh
python3 -m pip install -r requirements.txt
```

**Alternative installation methods:**
```zsh
# If python3 -m pip doesn't work, try:
pip3 install -r requirements.txt

# Or install Pillow directly:
python3 -m pip install Pillow

# If you're using conda:
conda install pillow

# If you're using homebrew's Python:
/usr/local/bin/python3 -m pip install Pillow
```

**Note for zsh users:** If `pip` command is not recognized, use `python3 -m pip` instead of just `pip`.

### Verify Installation

To check if everything is installed correctly:

```zsh
# Check Python version
python3 --version

# Check if Pillow is installed
python3 -c "from PIL import Image; print('Pillow is installed successfully')"

# Test the script
python3 image_converter.py --help
```

## Usage

### Basic Usage

Convert all JPG and PNG files in a folder (saves WebP files in a sibling "webp" folder):

```zsh
python3 image_converter.py /path/to/your/images
```

### Advanced Usage

**Specify output folder:**
```zsh
python3 image_converter.py /path/to/your/images -o /path/to/output/folder
```

**Set custom quality (0-100):**
```zsh
python3 image_converter.py /path/to/your/images --quality 90
```

**Combine options:**
```zsh
python3 image_converter.py /path/to/your/images -o /path/to/output --quality 75
```

### Examples

```zsh
# Convert images in current directory
python3 image_converter.py .

# Convert with high quality
python3 image_converter.py ./photos --quality 95

# Convert to separate output folder
python3 image_converter.py ~/Pictures/photos -o ~/Pictures/webp_output

# Show help
python3 image_converter.py --help
```

## Supported Formats

- **Input:** JPG, JPEG, PNG
- **Output:** WebP

## Features Details

- **Quality Control:** Adjust WebP compression quality (default: 80)
- **Transparency Handling:** PNG files with transparency are converted to RGB with white background
- **Error Handling:** Continues processing other files if one fails
- **Progress Indication:** Shows conversion progress with ✓ and ✗ symbols
- **Statistics:** Displays summary of successful and failed conversions

## Output

The app will:
1. Show the number of images found
2. Display input and output folders
3. Show conversion progress for each file
4. Provide a summary of results

Example output:
```
Found 5 image(s) to convert...
Input folder: /Users/username/photos
Output folder: /Users/username/webp
Quality: 80%
--------------------------------------------------
✓ Converted: IMG_001.jpg -> IMG_001.webp
✓ Converted: IMG_002.png -> IMG_002.webp
✗ Failed to convert IMG_003.jpg: cannot identify image file
✓ Converted: IMG_004.jpeg -> IMG_004.webp
✓ Converted: IMG_005.png -> IMG_005.webp
--------------------------------------------------
Conversion complete!
Total files: 5
Successfully converted: 4
Failed: 1
```

## Error Handling

The app handles various error conditions:
- Invalid input folder paths
- Corrupted image files
- Permission issues
- Insufficient disk space
- Keyboard interruption (Ctrl+C)

## License

This project is open source and available under the MIT License. 