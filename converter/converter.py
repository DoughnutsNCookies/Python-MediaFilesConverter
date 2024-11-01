import os
from PIL import Image
import pillow_heif
import subprocess
from concurrent.futures import ProcessPoolExecutor, as_completed

# Define the source and destination directories
SRC_DIR = 'src'
DST_DIR = 'dst'

# Ensure destination directory exists
os.makedirs(DST_DIR, exist_ok=True)

def convert_heic_to_png(input_path, output_path):
    """Convert HEIC files to JPEG."""
    heif_image = pillow_heif.open_heif(input_path)
    image = Image.frombytes(
        heif_image.mode, heif_image.size, heif_image.data, "raw", heif_image.mode
    )
    image.save(output_path, "JPEG")

def convert_dng_to_png(input_path, output_path):
    """Convert DNG files to JPEG."""
    image = Image.open(input_path)  # This may not work for all DNG files.
    image.save(output_path, "JPEG")

def convert_video(input_path, output_path):
    """Convert MOV video files to MP4 using ffmpeg."""
    try:
        command = ['ffmpeg', '-i', input_path, '-q:v', '0', output_path]
        subprocess.run(command, check=True)
        print(f"Converted: {input_path} to {output_path}")

    except subprocess.CalledProcessError as e:
        print(f"Error converting {input_path}: {e}")

def process_file(file_name):
    """Process a single file based on its extension."""
    src_file_path = os.path.join(SRC_DIR, file_name)
    dst_file_path = os.path.join(DST_DIR, file_name)
    file_ext = os.path.splitext(file_name)[1].lower()

    if file_ext == '.heic':
        dst_file_path = os.path.splitext(dst_file_path)[0] + '.png'
        convert_heic_to_png(src_file_path, dst_file_path)
    elif file_ext == '.dng':
        dst_file_path = os.path.splitext(dst_file_path)[0] + '.png'
        convert_dng_to_png(src_file_path, dst_file_path)
    elif file_ext == '.mov':
        dst_file_path = os.path.splitext(dst_file_path)[0] + '.mp4'
        convert_video(src_file_path, dst_file_path)
    else:
        # Copy non-target files directly to the destination
        os.makedirs(os.path.dirname(dst_file_path), exist_ok=True)
        with open(src_file_path, "rb") as src_file, open(dst_file_path, "wb") as dst_file:
            dst_file.write(src_file.read())

    return file_name, os.path.basename(dst_file_path)

def process_files():
    """Process files from src to dst directory with conversion."""
    with ProcessPoolExecutor() as executor:
        futures = {executor.submit(process_file, file_name): file_name for file_name in os.listdir(SRC_DIR)}

        for future in as_completed(futures):
            file_name = futures[future]
            try:
                processed_file_name, dst_file_name = future.result()
                print(f"Processed: {file_name} -> {dst_file_name}")
            except Exception as e:
                print(f"Failed to process {file_name}: {e}")

if __name__ == "__main__":
    process_files()
