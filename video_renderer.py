import json
import math
import shutil
import subprocess
import wave
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

OUT = Path("output")
WIDTH, HEIGHT = 540, 960
FPS = 12
import os
QUALITY = os.getenv("DINO_QUALITY", "1080p").lower()
SCALE = 4 if QUALITY in ("4k", "2160p", "uhd") else 2
FINAL_WIDTH, FINAL_HEIGHT = WIDTH * SCALE, HEIGHT * SCALE
EN_FONTS = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf",
]
HI_FONTS = [
    "/usr/share/fonts/truetype/noto/NotoSansDevanagari-Bold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansDevanagari-Regular.ttf",
]


class ScaledDraw:
    """Draw using 540x960 design coordinates on a native-resolution frame."""
    def __init__(self, draw, scale):
        self.draw, self.scale = draw, scale
    def _box(self, box):
        return tuple(round(v*self.scale) for v in box)
    def rounded_rectangle(self, box, radius=0, **kwargs):
        if "width" in kwargs: kwargs["width"] *= self.scale
        self.draw.rounded_rectangle(self._box(box), radius=radius*self.scale, **kwargs)
    def line(self, xy, **kwargs):
        if "width" in kwargs: kwargs["width"] *= self.scale
        self.draw.line([self._box(p) for p in xy], **kwargs)
    def ellipse(self, box, **kwargs):
        if "width" in kwargs: kwargs["width"] *= self.scale
        self.draw.ellipse(self._box(box), **kwargs)
    def arc(self, box, start, end, **kwargs):
        if "width" in kwargs: kwargs["width"] *= self.scale
        self.draw.arc(self._box(box), start, end, **kwargs)
    def polygon(self, xy, **kwargs):
        if "width" in kwargs: kwargs["width"] *= self.scale
        self.draw.polygon([self._box(p) for p in xy], **kwargs)
    def text(self, xy, text, **kwargs):
        if "stroke_width" in kwargs: kwargs["stroke_width"] *= self.scale
        self.draw.text(self._box(xy), text, **kwargs)
    def textbbox(self, xy, text, **kwargs):
        return tuple(round(v/self.scale) for v in self.draw.textbbox(self._box(xy), text, **kwargs))


def load_font(size, candidates, scale=1):
    for candidate in candidates:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size * scale)
    return ImageFont.load_default()


def wrap_text(draw, text, font, max_width):
    words = text.split()
    lines, current = [], ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if not current or draw.textbbox((0, 0), candidate, font=font)[2] <= max_width:
            current = candidate
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def centered_text(draw, text, y, font, fill, max_width=460, gap=5):
    for line in wrap_text(draw, text, font, max_width):
        box = draw.textbbox((0, 0), line, font=font, stroke_width=1)
        x = (WIDTH - (box[2] - box[0])) // 2
        draw.text((x, y), line, font=font, fill=fill,
                  stroke_width=1, stroke_fill=(25, 42, 55))
        y += box[3] - box[1] + gap
    return y


def background(draw, frame, scene_index):
    # Procedurally illustrated, original storybook landscape (no stock assets).
    for y in range(HEIGHT):
        t = y / HEIGHT
        color = (int(104 - 45*t), int(194 - 30*t), int(230 - 8*t))
        draw.line((0, y, WIDTH, y), fill=color)
    # Sun, soft clouds and layered hills
    draw.ellipse((405, 75, 490, 160), fill=(255, 222, 117), outline=(255, 245, 190), width=5)
    for x, y in [(45, 155), (250, 95), (360, 220)]:
        drift = int(8 * math.sin(frame / 9 + x))
        draw.ellipse((x+drift, y, x+85+drift, y+32), fill=(250, 255, 255))
        draw.ellipse((x+18+drift, y-20, x+58+drift, y+28), fill=(250, 255, 255))
    draw.ellipse((-100, 545, 350, 850), fill=(99, 190, 125))
    draw.ellipse((180, 520, 700, 880), fill=(68, 160, 112))
    # Trees with rounded leafy canopies
    for x, y in [(35, 485), (455, 490)]:
        draw.rectangle((x-8, y, x+15, y+155), fill=(126, 83, 55))
        draw.ellipse((x-52, y-68, x+62, y+48), fill=(43, 139, 91))
        draw.ellipse((x-32, y-100, x+45, y+20), fill=(62, 160, 98))
    # Foreground grass
    draw.rectangle((0, 760, WIDTH, HEIGHT), fill=(65, 153, 94))
    for i in range(22):
        x = (i * 47 + scene_index * 19) % WIDTH
        draw.line((x, 785, x-7, 765), fill=(155, 211, 115), width=3)


def draw_dino(draw, x, y, frame):
    bob = int(7 * math.sin(frame * 0.55))
    y += bob
    green, dark, belly = (105, 204, 130), (42, 125, 91), (218, 238, 167)
    # tail, body and neck
    draw.polygon([(x-85, y+45), (x-175, y+8), (x-125, y+95)], fill=green)
    draw.ellipse((x-90, y-20, x+92, y+145), fill=green, outline=dark, width=4)
    draw.rounded_rectangle((x+20, y-145, x+90, y+70), radius=30, fill=green, outline=dark, width=4)
    draw.ellipse((x-5, y-220, x+135, y-90), fill=green, outline=dark, width=4)
    # golden back spikes
    for i in range(4):
        sx = x - 65 + i*37
        draw.polygon([(sx, y-25-i%2*8), (sx+15, y-75-i%2*8), (sx+34, y-18)], fill=(255, 190, 77))
    draw.ellipse((x-48, y+35, x+52, y+125), fill=belly)
    # legs and animated waving arm
    stride = int(8 * math.sin(frame * 0.7))
    draw.ellipse((x-65, y+115+stride, x-5, y+150+stride), fill=dark)
    draw.ellipse((x+25, y+115-stride, x+85, y+150-stride), fill=dark)
    arm_y = int(16 * math.sin(frame * 0.6))
    draw.line((x+55, y+15, x+112, y+52+arm_y), fill=dark, width=13)
    draw.ellipse((x+103, y+42+arm_y, x+124, y+64+arm_y), fill=green)
    # expressive eyes and smile
    draw.ellipse((x+78, y-184, x+94, y-168), fill=(20, 45, 55))
    draw.ellipse((x+83, y-182, x+88, y-177), fill="white")
    draw.arc((x+65, y-157, x+120, y-115), 5, 115, fill=dark, width=4)


def draw_story_prop(draw, title, english, frame):
    key = (title + " " + english).lower()
    cx, cy = 270, 600
    bob = int(5 * math.sin(frame * .4))
    if any(k in key for k in ("block", "tower", "share")):
        for i, color in enumerate([(255, 116, 104), (255, 205, 78), (93, 173, 240)]):
            xx = 210 + (i % 2)*55
            yy = 515 - (i//2)*48 + bob
            draw.rounded_rectangle((xx, yy, xx+48, yy+48), radius=8, fill=color, outline="white", width=3)
    elif any(k in key for k in ("hand", "soap", "snack")):
        draw.rounded_rectangle((205, 510+bob, 335, 575+bob), radius=20, fill=(115, 207, 239), outline="white", width=4)
        draw.rounded_rectangle((235, 475+bob, 305, 520+bob), radius=12, fill=(255, 255, 255), outline=(70, 140, 180), width=3)
        for i in range(5):
            draw.ellipse((215+i*25, 455+(i%2)*18+bob, 230+i*25, 470+(i%2)*18+bob), fill=(235, 250, 255))
    elif any(k in key for k in ("plant", "garden", "water", "sunlight")):
        draw.rounded_rectangle((235, 610+bob, 310, 690+bob), radius=10, fill=(177, 105, 67))
        draw.line((272, 615+bob, 272, 500+bob), fill=(52, 130, 75), width=9)
        draw.ellipse((220, 500+bob, 275, 540+bob), fill=(85, 190, 95))
        draw.ellipse((270, 525+bob, 325, 565+bob), fill=(65, 170, 85))
    elif any(k in key for k in ("book", "help", "friend")):
        draw.polygon([(210, 520+bob), (270, 535+bob), (270, 620+bob), (210, 605+bob)], fill=(255, 218, 110), outline="white")
        draw.polygon([(270, 535+bob), (330, 520+bob), (330, 605+bob), (270, 620+bob)], fill=(115, 185, 245), outline="white")
        for yy in [555, 575, 595]:
            draw.line((222, yy+bob, 258, yy+8+bob), fill=(130, 95, 65), width=3)
            draw.line((282, yy+8+bob, 318, yy+bob), fill=(55, 105, 160), width=3)
    elif any(k in key for k in ("star", "draw", "practice")):
        points = []
        for i in range(10):
            radius = 62 if i % 2 == 0 else 27
            angle = -math.pi/2 + i*math.pi/5
            points.append((cx + math.cos(angle)*radius, 535+bob + math.sin(angle)*radius))
        draw.polygon(points, fill=(255, 211, 82), outline="white")
    else:
        draw.ellipse((235, 520+bob, 315, 600+bob), fill=(255, 210, 90), outline="white", width=4)


def draw_frame(title, english, hindi, scene_number, frame, total_frames, out_path):
    image = Image.new("RGB", (WIDTH, HEIGHT), (100, 180, 220))
    draw = ImageDraw.Draw(image)
    background(draw, frame, scene_number)
    # A small camera drift plus character bob creates motion between frames.
    dino_x = 265 + int(10 * math.sin(frame / 15))
    draw_story_prop(draw, title, english, frame)
    draw_dino(draw, dino_x, 635, frame)
    # Title ribbon
    draw.rounded_rectangle((22, 24, 518, 132), radius=25, fill=(24, 49, 78), outline=(255, 218, 115), width=4)
    title_font = load_font(27, EN_FONTS)
    centered_text(draw, title, 58, title_font, (255, 224, 133), 450, 4)
    # Bilingual caption panel with safe margins and readable type
    draw.rounded_rectangle((22, 790, 518, 930), radius=24, fill=(18, 42, 68), outline=(135, 205, 220), width=3)
    en_font = load_font(19, EN_FONTS)
    hi_font = load_font(19, HI_FONTS)
    centered_text(draw, english, 806, en_font, (255, 255, 255), 455, 2)
    draw.line((65, 861, 475, 861), fill=(100, 170, 190), width=2)
    centered_text(draw, hindi, 875, hi_font, (210, 240, 255), 455, 2)
    draw.text((468, 945), f"{scene_number}/3", font=load_font(15, EN_FONTS), fill="white")
    image.save(out_path, quality=92)


def scene_card(title, english, hindi, path, scene_number=1):
    """Backward-compatible full-HD poster render used by the pipeline tests."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    preview = path.with_name(path.stem + "_preview.png")
    draw_frame(title, english, hindi, scene_number, 0, 1, preview)
    with Image.open(preview) as image:
        image.resize((FINAL_WIDTH, FINAL_HEIGHT), Image.Resampling.LANCZOS).convert("RGB").save(path)
    preview.unlink(missing_ok=True)



def run_ffmpeg(args):
    subprocess.run(args, check=True)


def audio_duration(path):
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        check=True, capture_output=True, text=True,
    )
    return float(result.stdout.strip())


def make_original_music(path, duration):
    # Quiet, synthesized three-note ambient loop; no third-party music asset.
    sample_rate = 22050
    total = int(sample_rate * duration)
    notes = [(261.63, 329.63, 392.00), (293.66, 349.23, 440.00)]
    with wave.open(str(path), "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)
        chunk = bytearray()
        for i in range(total):
            t = i / sample_rate
            chord = notes[int(t // 4) % len(notes)]
            value = sum(math.sin(2*math.pi*f*t) for f in chord) / 3
            fade = min(1.0, t/0.8, (duration-t)/1.0)
            sample = int(32767 * 0.035 * max(0.0, fade) * value)
            chunk.extend(int(sample).to_bytes(2, "little", signed=True))
        wav.writeframes(chunk)


def render_scene(script_stem, title, scene, scene_number):
    en_audio = OUT / f"{script_stem}_scene{scene_number}_en.mp3"
    hi_audio = OUT / f"{script_stem}_scene{scene_number}_hi.mp3"
    for required in (en_audio, hi_audio):
        if not required.exists() or required.stat().st_size < 500:
            raise FileNotFoundError(f"Missing or empty narration: {required}")
    duration = audio_duration(en_audio) + audio_duration(hi_audio)
    frames_dir = OUT / f"{script_stem}_frames{scene_number}"
    frames_dir.mkdir(parents=True, exist_ok=True)
    frame_count = max(12, math.ceil(duration * FPS))
    blender = shutil.which("blender")
    if not blender:
        raise RuntimeError("Blender is required for genuine 3D rendering. Install Blender and retry.")
    project_root = Path(__file__).resolve().parent
    run_ffmpeg([blender, "--background", "--python", str(project_root / "blender_scene.py"),
                "--", str(frames_dir.resolve()), str(frame_count), QUALITY])
    # Blender can return exit code 0 even when its embedded Python script fails.
    # Verify the complete frame sequence before opening images or encoding video.
    expected_frames = [frames_dir / f"frame_{i:05d}.png" for i in range(frame_count)]
    missing_frames = [str(path) for path in expected_frames if not path.is_file()]
    if missing_frames:
        sample = ", ".join(missing_frames[:3])
        raise RuntimeError(
            f"Blender did not render {len(missing_frames)} of {frame_count} expected frames "
            f"for {script_stem} scene {scene_number}. Missing: {sample}. "
            "Check the Blender error immediately above this message."
        )
    # Add crisp bilingual story captions on top of the real 3D renders.
    title_font = load_font(25, EN_FONTS, SCALE)
    en_font = load_font(18, EN_FONTS, SCALE)
    hi_font = load_font(18, HI_FONTS, SCALE)
    for frame in range(frame_count):
        frame_path = frames_dir / f"frame_{frame:05d}.png"
        with Image.open(frame_path) as source:
            image = source.convert("RGB")
        draw = ScaledDraw(ImageDraw.Draw(image, "RGBA"), SCALE)
        draw.rounded_rectangle((18, 18, WIDTH-18, 112), radius=22,
                               fill=(20, 42, 66, 218), outline=(255, 213, 110, 255), width=3)
        centered_text(draw, title, 48, title_font, (255, 225, 140), WIDTH-70, 3)
        draw.rounded_rectangle((18, 785, WIDTH-18, 940), radius=22,
                               fill=(15, 34, 55, 225), outline=(130, 205, 220, 255), width=3)
        centered_text(draw, scene["en"], 800, en_font, (255,255,255), WIDTH-65, 2)
        draw.line((55, 860, WIDTH-55, 860), fill=(120,180,195,255), width=2)
        centered_text(draw, scene["hi"], 875, hi_font, (215,240,255), WIDTH-65, 2)
        draw.text((WIDTH-58, 945), f"{scene_number}/3", font=load_font(14, EN_FONTS), fill="white")
        image.save(frame_path)
    music = OUT / f"{script_stem}_scene{scene_number}_music.wav"
    make_original_music(music, duration + 0.5)
    part = OUT / f"{script_stem}_part{scene_number}.mp4"
    run_ffmpeg([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
        "-framerate", str(FPS), "-i", str(frames_dir / "frame_%05d.png"),
        "-i", str(en_audio), "-i", str(hi_audio), "-i", str(music),
        "-filter_complex",
        "[1:a][2:a]concat=n=2:v=0:a=1[narr];"
        "[3:a]volume=0.20[music];"
        "[narr][music]amix=inputs=2:duration=first:dropout_transition=1,"
        "afade=t=in:st=0:d=0.25,afade=t=out:st=" + str(max(0.1, duration-0.45)) + ":d=0.4[a]",
        "-map", "0:v:0", "-map", "[a]",
        "-vf", "fps=30,format=yuv420p,"
               f"fade=t=in:st=0:d=0.25,fade=t=out:st={max(0.1, duration-0.35)}:d=0.35",
        "-t", f"{duration:.3f}", "-c:v", "libx264", "-preset", "medium",
        "-crf", "19", "-c:a", "aac", "-b:a", "160k",
        "-movflags", "+faststart", str(part),
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
        parts = [render_scene(script.stem, data["title"], scene, index)
                 for index, scene in enumerate(scenes, start=1)]
        concat_file = OUT / f"{script.stem}_concat.txt"
        concat_file.write_text(
            "".join(f"file '{part.resolve()}'\n" for part in parts), encoding="utf-8"
        )
        final_video = OUT / f"{script.stem}.mp4"
        run_ffmpeg([
            "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
            "-f", "concat", "-safe", "0", "-i", str(concat_file),
            "-c:v", "libx264", "-preset", "medium",
            "-crf", "19", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart",
            str(final_video),
        ])
        print(f"Rendered animated video: {final_video}")


if __name__ == "__main__":
    main()
