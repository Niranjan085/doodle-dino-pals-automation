import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from PIL import Image, ImageChops

import daily_shorts
import video_renderer


class PipelineTests(unittest.TestCase):
    def test_story_generator_creates_three_bilingual_scripts(self):
        with tempfile.TemporaryDirectory() as folder:
            with patch.object(daily_shorts, "OUT", Path(folder)):
                daily_shorts.main()
            files = sorted(Path(folder).glob("short_*.json"))
            self.assertEqual(len(files), 3)
            for path in files:
                data = json.loads(path.read_text(encoding="utf-8"))
                self.assertEqual(len(data["scenes"]), 3)
                for scene in data["scenes"]:
                    self.assertTrue(scene["en"].strip())
                    self.assertTrue(scene["hi"].strip())

    def test_2d_cartoon_frames_are_animated(self):
        with tempfile.TemporaryDirectory() as folder:
            first = Path(folder) / "frame0.png"
            later = Path(folder) / "frame8.png"
            video_renderer.draw_frame("Dino Learns to Share", "Dino shares blocks.", "डिनो ब्लॉक्स बाँटता है।", 1, 0, 24, first)
            video_renderer.draw_frame("Dino Learns to Share", "Dino shares blocks.", "डिनो ब्लॉक्स बाँटता है।", 1, 8, 24, later)
            with Image.open(first) as a, Image.open(later) as b:
                self.assertIsNotNone(ImageChops.difference(a, b).getbbox())
    def test_scene_card_is_vertical_full_hd(self):
        with tempfile.TemporaryDirectory() as folder:
            target = Path(folder) / "scene.png"
            video_renderer.scene_card(
                "Dino Learns to Share",
                "Dino shares the blocks with a friend.",
                "डिनो अपने दोस्त के साथ ब्लॉक्स बाँटता है।",
                target,
            )
            with Image.open(target) as image:
                self.assertEqual(image.size, (video_renderer.FINAL_WIDTH, video_renderer.FINAL_HEIGHT))
                self.assertEqual(image.mode, "RGB")


if __name__ == "__main__":
    unittest.main()
