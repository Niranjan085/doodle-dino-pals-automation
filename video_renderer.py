import json
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT = Path("output")
W, H = 1080, 1920
FONTS = [
    "/usr/share/fonts/truetype/noto/NotoSansDevanagari-Regular.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
]

def font(size):
    for candidate in FONTS:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()

def wrap(draw, text, y, selected_font, fill, max_width=900):
    words, lines, current = text.split(), [], ""
    for word in words:
        test = (current + " " + word).strip()
        if draw.textbbox((0, 0), test, font=selected_font)[2] <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    for line in lines:
        box = draw.textbbox((0, 0), line, font=selected_font)
        x = (W - (box[2] - box[0])) // 2
        draw.text((x, y), line, font=selected_font, fill=fill,
                  stroke_width=2, stroke_fill=(8, 14, 30))
        y += selected_font.size + 18
    return y

def scene_card(title, en, hi, path):
    image = Image.new("RGB", (W, H), (20, 35, 65))
    draw = ImageDraw.Draw(image)
    draw.ellipse((760, 80, 1100, 420), fill=(45, 115, 130))
    draw.ellipse((60, 1450, 400, 1790), fill=(45, 115, 130))
    draw.rounded_rectangle((65, 300, 1015, 1620), radius=55, fill=(30, 55, 88))
    y = wrap(draw, title, 470, font(66), (255, 220, 105))
    y = wrap(draw, en, y + 90, font(48), "white")
    y += 70
    draw.line((180, y, 900, y), fill=(120, 190, 200), width=4)
    wrap(draw, hi, y + 75, font(48), (190, 235, 255))
    image.save(path)

def ffmpeg(args):
    subprocess.run(args, check=True)

def main():
    OUT.mkdir(exist_ok=True)
    scripts = sorted(OUT.glob("short_*.json"))
    if not scripts:
        raise FileNotFoundError("No scripts found; run daily_shorts.py first.")
    for script in scripts:
        data = json.loads(script.read_text(encoding="utf-8"))
        parts = []
        for i, scene in enumerate(data["scenes"], 1):
            picture = OUT / f"{script.stem}_{i}.png"
            scene_card(data["title"], scene["en"], scene["hi"], picture)
            en = OUT / f"{script.stem}_scene{i}_en.mp3"
            hi = OUT / f"{script.stem}_scene{i}_hi.mp3"
            for audio in (en, hi):
                if not audio.exists():
                    raise FileNotFoundError(f"Missing narration {audio}; run generate_voice.py.")
            part = OUT / f"{script.stem}_part{i}.mp4"
            ffmpeg(["ffmpeg", "-y", "-loop", "1", "-i", str(picture),
                    "-i", str(en), "-i", str(hi),
                    "-filter_complex", "[1:a][2:a]concat=n=2:v=0:a=1[a]",
                    "-map", "0:v", "-map", "[a]", "-c:v", "libx264",
                    "-tune", "stillimage", "-c:a", "aac", "-b:a", "128k",
                    "-shortest", "-pix_fmt", "yuv420p", "-r", "30",
                    "-vf", "scale=1080:1920,format=yuv420p", str(part)])
            parts.append(part)
        concat = OUT / f"{script.stem}_concat.txt"
        concat.write_text("".join(f"file '{p.resolve()}'\n" for p in parts), encoding="utf-8")
        final = OUT / f"{script.stem}.mp4"
        ffmpeg(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat),
                "-c", "copy", "-movflags", "+faststart", str(final)])
        print("Rendered bilingual video:", final)

if __name__ == "__main__":
    main()
