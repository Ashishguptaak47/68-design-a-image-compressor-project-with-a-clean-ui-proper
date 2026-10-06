import os
import shutil
import unittest
from PIL import Image
from main import compress_image, INPUT_DIR, OUTPUT_DIR, ensure_folders

class TestImageCompressor(unittest.TestCase):
    def setUp(self):
        ensure_folders()
        self.test_img_path = os.path.join(INPUT_DIR, "test_sample.jpg")
        img = Image.new('RGB', (800, 800), color='red')
        img.save(self.test_img_path, "JPEG")

    def tearDown(self):
        if os.path.exists(INPUT_DIR):
            shutil.rmtree(INPUT_DIR)
        if os.path.exists(OUTPUT_DIR):
            shutil.rmtree(OUTPUT_DIR)

    def test_compress_image(self):
        ensure_folders()
        out_path = os.path.join(OUTPUT_DIR, "test_sample_compressed.jpg")
        size = compress_image(self.test_img_path, out_path, quality=50)
        self.assertTrue(size > 0)
        self.assertTrue(os.path.exists(out_path))

if __name__ == '__main__':
    unittest.main()
