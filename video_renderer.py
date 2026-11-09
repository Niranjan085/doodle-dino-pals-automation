import json
import math
import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

OUT = Path("output")
WIDTH, HEIGHT = 1080, 1920
EN_FONTS = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf",
]
HI_FONTS = [
    "/usr/share/fonts/truetype/noto/NotoSansDevanagari-Bold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansDevanagari-Regular.ttf",
]


def load_font(size, candidates):
    for candidate in candidates:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


def wrap_text(draw, text, font, max_width):
    words = text.split()
    lines, current = [], ""
    for word in words:
        trial = f"{current} {word}".strip()
        if not current or draw.textbbox((0, 0), trial, font=font)[2] <= max_width:
            current = trial
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_centered_lines(draw, text, top, font, fill, max_width=900, line_gap=18):
    y = top
    for line in wrap_text(draw, text, font, max_width):
        box = draw.textbbox((0, 0), line, font=font, stroke_width=1)
        x = (WIDTH - (box[2] - box[0])) // 2
        draw.text((x, y), line, font=font, fill=fill,
                  stroke_width=1, stroke_fill=(10, 25, 40))
        y += box[3] - box[1] + line_gap
    return y


def draw_dino(draw, center_x=540, center_y=850, scale=1.0, pose=0):
    # Friendly original dinosaur mascot made from simple vector shapes.
    s = scale
    green = (105, 205, 135)
    dark = (35, 115, 85)
    belly = (205, 240, 170)
    # Tail and feet
    draw.polygon([(int(center_x-220*s), int(center_y+80*s)),
                  (int(center_x-390*s), int(center_y+10*s)),
                  (int(center_x-285*s), int(center_y+180*s))], fill=green)
    draw.ellipse((int(center_x-150*s), int(center_y+160*s),
                  int(center_x-15*s), int(center_y+245*s)), fill=dark)
    draw.ellipse((int(center_x+20*s), int(center_y+160*s),
                  int(center_x+155*s), int(center_y+245*s)), fill=dark)
    # Body, neck and head
    draw.ellipse((int(center_x-235*s), int(center_y-90*s),
                  int(center_x+235*s), int(center_y+220*s)), fill=green)
    draw.rounded_rectangle((int(center_x+45*s), int(center_y-260*s),
                            int(center_x+205*s), int(center_y+80*s)),
                           radius=int(70*s), fill=green)
    draw.ellipse((int(center_x-10*s), int(center_y-430*s),
                  int(center_x+300*s), int(center_y-150*s)), fill=green)
    # Back spikes
    for i in range(4):
        x = center_x - 130*s + i*82*s
        y = center_y - 145*s - (i % 2)*20*s
        draw.polygon([(int(x), int(y)), (int(x+35*s), int(y-95*s)),
                      (int(x+75*s), int(y+5*s))], fill=(255, 190, 85))
    # Belly patch and face
    draw.ellipse((int(center_x-115*s), int(center_y+5*s),
                  int(center_x+125*s), int(center_y+185*s)), fill=belly)
    draw.ellipse((int(center_x+165*s), int(center_y-325*s),
                  int(center_x+195*s), int(center_y-295*s)), fill=(20, 45, 55))
    draw.ellipse((int(center_x+245*s), int(center_y-250*s),
                  int(center_x+275*s), int(center_y-220*s)), fill=(255, 255, 255))
    draw.arc((int(center_x+155*s), int(center_y-260*s),
              int(center_x+265*s), int(center_y-175*s)),
             start=10, end=100, fill=dark, width=max(3, int(7*s)))
    # Little arms
    draw.line((int(center_x+80*s), int(center_y+15*s),
               int(center_x+210*s), int(center_y+75*s)),
              fill=dark, width=max(8, int(24*s)))
    draw.line((int(center_x+210*s), int(center_y+75*s),
               int(center_x+250*s), int(center_y+35*s)),
              fill=dark, width=max(8, int(24*s)))


def scene_card(title, english, hindi, path, scene_number=1):
    image = Image.new("RGB", (WIDTH, HEIGHT))
    pixels = image.load()
    top = (20, 48, 86)
    bottom = (76, 145, 145)
    for y in range(HEIGHT):
        ratio = y / (HEIGHT - 1)
        color = tuple(int(top[i] * (1-ratio) + bottom[i] * ratio) for i in range(3))
        ImageDraw.Draw(image).line((0, y, WIDTH, y), fill=color)

    draw = ImageDraw.Draw(image)
    # Decorative sky bubbles and simple landscape.
    for x, y, radius in [(120, 230, 36), (930, 320, 52), (870, 1160, 28), (170, 1300, 22)]:
        draw.ellipse((x-radius, y-radius, x+radius, y+radius), fill=(145, 210, 205))
    draw.ellipse((-180, 1470, 1260, 2140), fill=(55, 135, 105))
    draw.rounded_rectangle((55, 90, 1025, 430), radius=55, fill=(17, 38, 69))
    title_font = load_font(58, EN_FONTS)
    draw_centered_lines(draw, title, 170, title_font, (255, 220, 115), 850, 16)
    draw_dino(draw, center_y=900, scale=1.0, pose=scene_number)

    # Readable bilingual caption panel.
    draw.rounded_rectangle((55, 1260, 1025, 1810), radius=48, fill=(17, 38, 69))
    en_font = load_font(43, EN_FONTS)
    hi_font = load_font(43, HI_FONTS)
    draw_centered_lines(draw, english, 1335, en_font, (255, 255, 255), 850, 12)
    draw.line((180, 1535, 900, 1535), fill=(110, 190, 190), width=4)
    draw_centered_lines(draw, hindi, 1600, hi_font, (205, 240, 255), 850, 12)
    draw.text((WIDTH-180, HEIGHT-90), f"{scene_number}/3",
              font=load_font(28, EN_FONTS), fill=(255, 255, 255))
    image.save(path, quality=95)


def run_ffmpeg(args):
    subprocess.run(args, check=True)


def audio_duration(path):
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        check=True, capture_output=True, text=True,
    )
    return float(result.stdout.strip())


def render_scene(script_stem, title, scene, scene_number):
    picture = OUT / f"{script_stem}_scene{scene_number}.png"
    english_audio = OUT / f"{script_stem}_scene{scene_number}_en.mp3"
    hindi_audio = OUT / f"{script_stem}_scene{scene_number}_hi.mp3"
    for required in (english_audio, hindi_audio):
        if not required.exists() or required.stat().st_size < 500:
            raise FileNotFoundError(f"Missing or empty narration: {required}")

    scene_card(title, scene["en"], scene["hi"], picture, scene_number)
    combined_duration = audio_duration(english_audio) + audio_duration(hindi_audio)
    frames = max(1, math.ceil(combined_duration * 30))
    part = OUT / f"{script_stem}_part{scene_number}.mp4"
    run_ffmpeg([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
        "-loop", "1", "-framerate", "30", "-i", str(picture),
        "-i", str(english_audio), "-i", str(hindi_audio),
        "-filter_complex", "[1:a][2:a]concat=n=2:v=0:a=1[a]",
        "-map", "0:v:0", "-map", "[a]",
        "-vf", f"zoompan=z='min(zoom+0.00035,1.06)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s={WIDTH}x{HEIGHT}:fps=30,format=yuv420p",
        "-frames:v", str(frames), "-c:v", "libx264", "-preset", "veryfast",
        "-crf", "23", "-c:a", "aac", "-b:a", "128k",
        "-shortest", "-movflags", "+faststart", str(part),
    ])
    return part


def main():
    if shutil.which("ffmpeg") is None or shutil.which("ffprobe") is None:
        raise RuntimeError("FFmpeg and ffprobe must be installed and available on PATH.")
    OUT.mkdir(parents=True, exist_ok=True)
    scripts = sorted(OUT.glob("short_*.json"))
    if len(scripts) != 3:
        raise RuntimeError(f"Expected exactly 3 story scripts; found {len(scripts)}.")

    for script in scripts:
        data = json.loads(script.read_text(encoding="utf-8"))
        scenes = data.get("scenes", [])
        if len(scenes) != 3:
            raise ValueError(f"{script.name} must contain exactly 3 scenes.")
        parts = [
            render_scene(script.stem, data["title"], scene, index)
            for index, scene in enumerate(scenes, start=1)
        ]
        concat_file = OUT / f"{script.stem}_concat.txt"
        concat_file.write_text(
            "".join(f"file '{part.resolve()}'\n" for part in parts),
            encoding="utf-8",
        )
        final_video = OUT / f"{script.stem}.mp4"
        run_ffmpeg([
            "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
            "-f", "concat", "-safe", "0", "-i", str(concat_file),
            "-c", "copy", "-movflags", "+faststart", str(final_video),
        ])
        print(f"Rendered video: {final_video}")


if __name__ == "__main__":
    main()
