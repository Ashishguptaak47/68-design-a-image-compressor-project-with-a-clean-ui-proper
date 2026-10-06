import os
import sys
from PIL import Image

INPUT_DIR = "input"
OUTPUT_DIR = "output"

def ensure_folders():
    os.makedirs(INPUT_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

def compress_image(input_path: str, output_path: str, quality: int = 85, max_size: tuple = None) -> int:
    try:
        with Image.open(input_path) as img:
            if max_size:
                img.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            rgb_img = img.convert('RGB')
            rgb_img.save(output_path, "JPEG", quality=quality, optimize=True)
            return os.path.getsize(output_path)
    except Exception as e:
        print(f"Error processing {input_path}: {e}", file=sys.stderr)
        return -1

def batch_compress(quality: int = 80, max_width: int = 1920, max_height: int = 1080):
    ensure_folders()
    valid_extensions = (".jpg", ".jpeg", ".png", ".bmp", ".webp")
    files = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith(valid_extensions)]
    
    if not files:
        print(f"No images found in '{INPUT_DIR}/'. Please add some images and run again.")
        return

    print(f"Found {len(files)} image(s) to compress.")
    for filename in files:
        in_path = os.path.join(INPUT_DIR, filename)
        name, _ = os.path.splitext(filename)
        out_filename = f"{name}_compressed.jpg"
        out_path = os.path.join(OUTPUT_DIR, out_filename)

        orig_size = os.path.getsize(in_path)
        new_size = compress_image(in_path, out_path, quality=quality, max_size=(max_width, max_height))
        
        if new_size != -1:
            savings = ((orig_size - new_size) / orig_size) * 100 if orig_size > 0 else 0
            print(f"[SUCCESS] {filename} -> {out_filename} | Size: {orig_size//1024}KB -> {new_size//1024}KB ({savings:.1f}% reduction)")

if __name__ == "__main__":
    print("--- Python Image Compressor ---")
    batch_compress(quality=75)
