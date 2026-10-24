import io
import struct
import unittest
from unittest.mock import patch

from PIL import Image


class GifSeekSecurityTests(unittest.TestCase):
    def test_rejected_frame_does_not_change_image_size(self):
        # Exercise CVE-2026-112400 with a low pixel limit and a small extent.
        # Never retry load() or allocate using the rejected dimensions.
        frame = (
            b"," + struct.pack("<HHHHB", 0, 0, 1, 1, 0)
            + b"\x02\x02\x44\x01\x00"
        )
        gif = (
            b"GIF89a" + struct.pack("<HHBBB", 1, 1, 0x80, 0, 0)
            + b"\x00" * 3 + b"\xff" * 3
            + frame
            + b"," + struct.pack("<HHHHB", 0, 0, 256, 256, 0)
            + frame + b";"
        )
        with patch.object(Image, "MAX_IMAGE_PIXELS", 1024):
            with Image.open(io.BytesIO(gif)) as image:
                original_size = image.size
                with self.assertRaises(Image.DecompressionBombError):
                    image.seek(1)
                self.assertEqual(image.size, original_size)

    def test_valid_animation_can_still_seek_and_decode(self):
        gif = io.BytesIO()
        with Image.new("RGB", (2, 2), "red") as first:
            with Image.new("RGB", (2, 2), "blue") as second:
                first.save(
                    gif, format="GIF", save_all=True,
                    append_images=[second], duration=50, loop=0,
                )
        gif.seek(0)
        with Image.open(gif) as image:
            self.assertEqual(image.n_frames, 2)
            image.seek(1)
            image.load()
            self.assertEqual(image.size, (2, 2))
            self.assertEqual(image.convert("RGB").getpixel((0, 0)), (0, 0, 255))


if __name__ == "__main__":
    unittest.main()
