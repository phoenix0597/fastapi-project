import importlib
import os
from pathlib import Path
import sys
import tempfile
from types import ModuleType, SimpleNamespace
import unittest
from unittest.mock import patch

from PIL import Image


class ImageTaskCompatibilityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Import the real Celery task without loading .env, DB or SMTP secrets.
        config = ModuleType("app.config")
        config.settings = SimpleNamespace(
            REDIS_HOST="127.0.0.1", REDIS_PORT=1,
            SMTP_USER="image-tests@example.invalid",
        )
        with patch.dict(sys.modules, {"app.config": config}):
            cls.task = importlib.import_module("app.tasks.tasks").process_pic

    def test_real_resize_task_preserves_output_sizes_and_formats(self):
        previous_directory = Path.cwd()
        with tempfile.TemporaryDirectory(prefix="pillow-image-task-") as folder:
            root = Path(folder)
            (root / "app/static/images").mkdir(parents=True)
            (root / "uploads").mkdir()
            try:
                os.chdir(root)
                for extension, image_format in (
                    ("png", "PNG"), ("jpg", "JPEG"),
                    ("webp", "WEBP"), ("gif", "GIF"),
                ):
                    with self.subTest(format=image_format):
                        # The upload route stores all input formats as .webp.
                        source = root / "uploads" / f"hotel-{extension}.webp"
                        with Image.new("RGB", (16, 12), "red") as image:
                            image.save(source, format=image_format)

                        # Run synchronously: no broker, worker or email calls.
                        self.task.run(str(source))
                        for width, height in ((1024, 768), (200, 150)):
                            output = root / "app/static/images" / (
                                f"{width}_{height}{source.name}"
                            )
                            with Image.open(output) as resized:
                                resized.load()
                                self.assertEqual(resized.size, (width, height))
                                self.assertEqual(resized.format, "WEBP")
            finally:
                os.chdir(previous_directory)


if __name__ == "__main__":
    unittest.main()
