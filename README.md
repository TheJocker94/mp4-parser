# MP4 Image Extractor

This Python script extracts images from 'mdat' boxes in MP4 files encoded in Base64 within XML.

The code instruction for this script are in the pdf file.

## Usage

1. Install dependencies using `pip`:
   ```bash
   pip install -r requirements.txt
2. Run the script with the desired MP4 file(s):
   ```bash
   python parser_mp4.py <file_path1> <file_path2> ...
## Dependencies
Pillow (PIL Fork): Python Imaging Library (PIL) fork for image processing.
## Script Overview
 * ### read_box(file):
   Reads the size and box type from the MP4 file.
 * ### parse_box(file):
   Parses MP4 boxes, identifies 'mdat' boxes, and processes their content.
 * ### process_mdat(file, size, indentation):
   Processes the content of 'mdat' boxes, decoding UTF-8 content, and extracting images.
 * ### extract_images(xml_content, output_folder="."):
   Extracts images from the decoded XML content.
 * ### process_file(file_path):
   Processes the specified MP4 file and handles errors.
 * ### main():
   Main function to handle command-line arguments and process multiple files.
## Output
- The script prints information about the mp4 file and its structure.
- If a box of type MDAT is found, extract and print the content of that box.
- Extracted images are saved in the current folder.
### Notes
Only supports MP4 files.
Images are expected to be encoded in Base64 within SMPTE-TT XML in 'mdat' boxes.
