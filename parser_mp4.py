import struct
import xml.etree.ElementTree as ET
import base64
from io import BytesIO
from PIL import Image
import sys
import os

# Function to read the size and box type from the MP4 file
def read_box(file):
    data = file.read(4)
    if len(data) < 4:
        return None, None
    size = struct.unpack('>I', data)[0]
    box_type = file.read(4).decode('latin-1')
    return size, box_type

# Function to parse the MP4 boxes and identify 'mdat' boxes for further processing
def parse_box(file):
    stack = []

    while True:
        position = file.tell()
        size, box_type = read_box(file)

        if size is None or box_type is None:
            break  # End of file

        indentation = len(stack) * 4
        print(f"{' ' * indentation}Box ID: \033[92m{box_type}\033[0m of size {size}")

        if box_type in {'moof', 'traf'}:
            # Box contains other boxes
            stack.append(position + size - 8)
        elif box_type == 'mdat':
            process_mdat(file, size, indentation)
        else:
            # All other boxes
            file.seek(size - 8, os.SEEK_CUR)

        # Process boxes in the stack
        while stack and file.tell() >= stack[-1]:
            stack.pop()

# Function to process the content of 'mdat' boxes, decoding UTF-8 content and extracting images
def process_mdat(file, size, indentation):
    mdat_content = file.read(size - 8)
    try:
        decoded_content = mdat_content.decode('utf-8')
        mdat_header = f"\033[92m{' ' * indentation}Mdat content:\n\033[0m"
        print(mdat_header + decoded_content)
        extract_images(decoded_content)
    except UnicodeDecodeError:
        mdat_error_message = f"\033[93m{' ' * indentation}Mdat content non utf-8\033[0m"
        print(mdat_error_message)

# Function to extract images from the decoded XML content
def extract_images(xml_content, output_folder="."):
    root = ET.fromstring(xml_content)

    # Define the namespace map
    namespace_map = {"smpte": "http://www.smpte-ra.org/schemas/2052-1/2010/smpte-tt"}

    # Find all image elements using the namespace map
    image_elements = root.findall(".//smpte:image", namespaces=namespace_map)
    
    for image_element in image_elements:
        # Extract image ID and type
        image_id = image_element.get("{http://www.w3.org/XML/1998/namespace}id")
        image_type = image_element.get("imagetype")
        # Decode base64-encoded image data
        image_data = base64.b64decode(image_element.text)
        # Create an image from the decoded data
        image = Image.open(BytesIO(image_data))
        # Save the image
        image.save(f"{image_id}.{image_type.lower()}")
        print(f"\033[93mSaved: {image_id}.{image_type.lower()} in current folder\033[0m")

# Function to process the specified MP4 file and handle errors
def process_file(file_path):
    if not os.path.exists(file_path):
        print("\033[91mError: File not found: {}\033[0m".format(file_path))
        return

    _, file_extension = os.path.splitext(file_path)
    if file_extension.lower() != ".mp4":
        error_message = "\033[91mError: Unsupported file format. Expected '.mp4' but got '{}'.\033[0m".format(file_extension)
        print(error_message)
        return

    processing_message = "\033[92mProcessing file: {}\033[0m".format(file_path)
    print(processing_message)

    with open(file_path, 'rb') as file:
        parse_box(file)

    end_message = "\033[92m" + "=" * 40 + "ENDFILE" + "=" * 40 + "\033[0m"
    print(end_message)

# Main function to handle command-line arguments and process multiple files
def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py <file_path1> <file_path2> ...")
        sys.exit(1)

    for file_path in sys.argv[1:]:
        process_file(file_path)

if __name__ == "__main__":
    main()