import tempfile
import unittest
from pathlib import Path

from PIL import Image, UnidentifiedImageError
import pillow_heif

from heic_to_jpg import convert


class ConversionTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)

    def test_real_heic_conversion_preserves_source(self):
        source = self.root / "sample.heic"
        pillow_heif.from_pillow(Image.new("RGB", (40, 30), (200, 80, 30))).save(source)
        before = source.read_bytes()
        result = convert(source, self.root)
        with Image.open(result) as image:
            self.assertEqual(image.format, "JPEG")
            self.assertEqual(image.size, (40, 30))
            self.assertEqual(image.mode, "RGB")
            self.assertTrue(all(abs(a - b) < 8 for a, b in zip(image.getpixel((20, 15)), (200, 80, 30))))
        self.assertEqual(source.read_bytes(), before)

    def test_existing_outputs_are_never_overwritten(self):
        source = self.root / "photo.heic"
        pillow_heif.from_pillow(Image.new("RGB", (16, 16))).save(source)
        for filename in ("photo.jpg", "photo_1.jpg"):
            (self.root / filename).write_bytes(b"existing")
        self.assertEqual(convert(source, self.root).name, "photo_2.jpg")
        for filename in ("photo.jpg", "photo_1.jpg"):
            self.assertEqual((self.root / filename).read_bytes(), b"existing")

    def test_invalid_input_leaves_no_output(self):
        source = self.root / "broken.heic"
        source.write_bytes(b"not an image")
        with self.assertRaises((UnidentifiedImageError, ValueError, OSError)):
            convert(source, self.root)
        self.assertEqual(list(self.root.glob("*.jpg")), [])

    def test_orientation_is_applied_and_metadata_removed(self):
        # TIFF preserves the synthetic orientation tag for a deterministic test.
        source = self.root / "rotated.tiff"
        image = Image.new("RGB", (40, 20), "red")
        exif = Image.Exif()
        exif[274] = 6
        exif[270] = "private test metadata"
        image.save(source, exif=exif)
        result = convert(source, self.root)
        with Image.open(result) as output:
            self.assertEqual(output.size, (20, 40))
            self.assertEqual(len(output.getexif()), 0)

    def test_transparent_pixels_become_white(self):
        source = self.root / "transparent.png"
        Image.new("RGBA", (16, 16), (255, 0, 0, 0)).save(source)
        with Image.open(convert(source, self.root)) as output:
            self.assertTrue(all(channel >= 250 for channel in output.getpixel((8, 8))))


if __name__ == "__main__":
    unittest.main()
