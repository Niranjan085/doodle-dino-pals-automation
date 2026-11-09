from pathlib import Path
import json, subprocess, shutil
from PIL import Image, ImageDraw, ImageFont

OUT = Path("output")
W, H, FPS = 720, 1280, 24

def font(size, bold=False):
    p = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    return ImageFont.truetype(p, size) if Path(p).exists() else ImageFont.load_default()

def wrap(draw, text, fnt, width):
    lines, line = [], ""
    for word in text.split():
        trial = (line + " " + word).strip()
        if draw.textbbox((0,0), trial, font=fnt)[2] <= width:
            line = trial
        else:
            if line: lines.append(line)
            line = word
    if line: lines.append(line)
    return lines

def centered(draw, text, y, fnt, color):
    for line in wrap(draw, text, fnt, 610):
        box = draw.textbbox((0,0), line, font=fnt)
        draw.text(((W-(box[2]-box[0]))//2, y), line, font=fnt, fill=color)
        y += box[3]-box[1]+10
    return y

def render_card(scene, number, path):
    im = Image.new("RGB", (W,H), (17,35,67))
    d = ImageDraw.Draw(im)
    d.ellipse((220,105,500,385), fill=(72,180,145), outline="white", width=8)
    d.ellipse((292,195,330,233), fill="white")
    d.ellipse((390,195,428,233), fill="white")
    d.arc((305,230,415,320), 5, 175, fill="white", width=8)
    d.ellipse((250,75,345,175), fill=(72,180,145))
    d.ellipse((410,75,505,175), fill=(72,180,145))
    d.rounded_rectangle((30,430,690,1160), radius=35, fill="white")
    d.rounded_rectangle((65,465,655,535), radius=22, fill=(255,210,80))
    d.text((88,485), f"DOODLE DINO PALS  •  SHORT {number}/3", font=font(22,True), fill=(25,42,65))
    y = centered(d, scene["on_screen_text"], 575, font(36,True), (17,100,90)) + 22
    y = centered(d, scene["english"], y, font(25), (25,42,65)) + 20
    centered(d, scene["hindi"], y, font(25), (25,42,65))
    d.text((235,1190), "LEARN • PLAY • DISCOVER!", font=font(20,True), fill="white")
    im.save(path, quality=92)

def run(args):
    subprocess.run(args, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)

def main():
    if not shutil.which("ffmpeg"):
        raise RuntimeError("FFmpeg is missing")
    scripts = sorted(OUT.glob("*_short_[123].json"))
    if len(scripts) != 3:
        raise RuntimeError(f"Expected 3 scripts, found {len(scripts)}")
    for f in scripts:
        data = json.loads(f.read_text(encoding="utf-8"))
        n = data["number"]
        work = OUT / f"render_{n}"
        work.mkdir(exist_ok=True)
        clips = []
        for i, scene in enumerate(data["scenes"], 1):
            img = work / f"frame{i}.jpg"
            audio = f.with_name(f.stem + f"_scene{i}.mp3")
            if not audio.exists():
                raise RuntimeError(f"Missing {audio.name}")
            render_card(scene, n, img)
            clip = work / f"clip{i}.mp4"
            run(["ffmpeg","-y","-loop","1","-i",str(img),"-i",str(audio),
                 "-vf",f"scale={W}:{H},format=yuv420p","-c:v","libx264",
                 "-tune","stillimage","-c:a","aac","-b:a","128k",
                 "-shortest","-r",str(FPS),"-pix_fmt","yuv420p",str(clip)])
            clips.append(clip)
        listing = work / "concat.txt"
        listing.write_text("".join(f"file '{p.resolve()}'\n" for p in clips))
        final = OUT / f.stem.replace(".json",".mp4")
        run(["ffmpeg","-y","-f","concat","-safe","0","-i",str(listing),
             "-c","copy","-movflags","+faststart",str(final)])
        print("Created", final)
    print("Done: 3 vertical MP4 files.")
if __name__ == "__main__":
    main()
