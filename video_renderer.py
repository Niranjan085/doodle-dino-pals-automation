import json
import subprocess
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

OUT = Path("output")
W, H = 1080, 1920


def font(size):
    for path in [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/noto/NotoSansDevanagari-Regular.ttf",
    ]:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def card(text, path):
    image = Image.new("RGB", (W, H), (20, 35, 65))
    draw = ImageDraw.Draw(image)
    draw.ellipse((760, 80, 1100, 420), fill=(45, 115, 130))
    draw.ellipse((60, 1450, 400, 1790), fill=(45, 115, 130))
    selected_font = font(64)
    lines = []
    for paragraph in text.splitlines() or [text]:
        lines += textwrap.wrap(paragraph, width=24) or [""]
    y = H // 2 - (len(lines) * 85) // 2
    for line in lines:
        bounds = draw.textbbox((0, 0), line, font=selected_font)
        x = (W - (bounds[2] - bounds[0])) // 2
        draw.text(
            (x, y), line, font=selected_font, fill="white",
            stroke_width=2, stroke_fill=(5, 10, 20)
        )
        y += 85
    image.save(path)


def main():
    OUT.mkdir(exist_ok=True)
    for json_file in sorted(OUT.glob("short_*.json")):
        data = json.loads(json_file.read_text(encoding="utf-8"))
        frames = []
        parts = []

        for index, scene in enumerate(data["scenes"], 1):
            image_path = OUT / f"{json_file.stem}_{index}.png"
            card(scene["en"], image_path)
            frames.append(image_path)

        for index, image_path in enumerate(frames, 1):
            audio_path = OUT / f"{json_file.stem}_scene{index}_en.mp3"
            if not audio_path.exists():
                raise FileNotFoundError(
                    f"Missing narration: {audio_path}. Run generate_voice.py first."
                )

            part_path = OUT / f"{json_file.stem}_part{index}.mp4"
            subprocess.run(
                [
                    "ffmpeg", "-y", "-loop", "1", "-i", str(image_path),
                    "-i", str(audio_path), "-c:v", "libx264",
                    "-tune", "stillimage", "-c:a", "aac", "-b:a", "128k",
                    "-shortest", "-pix_fmt", "yuv420p", "-r", "30",
                    str(part_path),
                ],
                check=True,
            )
            parts.append(part_path)

        concat_file = OUT / f"{json_file.stem}_concat.txt"
        concat_file.write_text(
            "".join(f"file '{part.resolve()}'\n" for part in parts),
            encoding="utf-8",
        )

        final_path = OUT / f"{json_file.stem}.mp4"
        subprocess.run(
            [
                "ffmpeg", "-y", "-f", "concat", "-safe", "0",
                "-i", str(concat_file), "-c", "copy",
                "-movflags", "+faststart", str(final_path),
            ],
            check=True,
        )
        print("Rendered", final_path)


if __name__ == "__main__":
    main()
