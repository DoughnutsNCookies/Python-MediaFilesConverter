import os
from PIL import Image
import pillow_heif
from moviepy.editor import VideoFileClip

# Define the source and destination directories
SRC_DIR = 'src'
DST_DIR = 'dst'

# Ensure destination directory exists
os.makedirs(DST_DIR, exist_ok=True)

def convert_heic_to_png(input_path, output_path):
    """Convert HEIC files to PNG."""
    heif_image = pillow_heif.open_heif(input_path)
    image = Image.frombytes(
        heif_image.mode, heif_image.size, heif_image.data, "raw", heif_image.mode
    )
    image.save(output_path, "PNG")

def convert_dng_to_png(input_path, output_path):
    """Convert DNG files to PNG."""
    # Note: DNG files can be complex. This uses Pillow for demonstration.
    # If you have trouble with DNG, consider using a dedicated library or tool.
    image = Image.open(input_path)  # This may not work for all DNG files.
    image.save(output_path, "PNG")

def convert_video(input_path, output_path):
    """Convert MOV video files to MP4."""
    clip = VideoFileClip(input_path)
    clip.write_videofile(output_path, codec="libx264")
    clip.close()

def process_files():
    """Process files from src to dst directory with conversion."""
    for root, _, files in os.walk(SRC_DIR):
        for file_name in files:
            src_file_path = os.path.join(root, file_name)
            dst_file_path = os.path.join(DST_DIR, file_name)
            file_ext = os.path.splitext(file_name)[1].lower()

            try:
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

                print(f"Processed: {file_name} -> {os.path.basename(dst_file_path)}")

            except Exception as e:
                print(f"Failed to process {file_name}: {e}")

if __name__ == "__main__":
    process_files()
