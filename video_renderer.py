import json, subprocess, textwrap
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
OUT=Path("output"); W,H=1080,1920
def font(size):
 for p in ["/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf","/usr/share/fonts/truetype/noto/NotoSansDevanagari-Regular.ttf"]:
  if Path(p).exists(): return ImageFont.truetype(p,size)
 return ImageFont.load_default()
def card(text,path):
 im=Image.new("RGB",(W,H),(20,35,65)); d=ImageDraw.Draw(im)
 d.ellipse((760,80,1100,420),fill=(45,115,130)); d.ellipse((60,1450,400,1790),fill=(45,115,130))
 f=font(64); lines=[]
 for para in text.splitlines() or [text]:
  lines+=textwrap.wrap(para,width=24) or [""]
 y=H//2-(len(lines)*85)//2
 for line in lines:
  box=d.textbbox((0,0),line,font=f); x=(W-(box[2]-box[0]))//2
  d.text((x,y),line,font=f,fill="white",stroke_width=2,stroke_fill=(5,10,20)); y+=85
 im.save(path)
def main():
 for jf in sorted(OUT.glob("short_*.json")):
  data=json.loads(jf.read_text(encoding="utf-8")); frames=[]
  for i,s in enumerate(data["scenes"],1):
   img=OUT/f"{jf.stem}_{i}.png"; card(s["en"],img); frames.append(img)
  # make one simple vertical video with per-scene image/audio segments
  parts=[]
  for i,img in enumerate(frames,1):
   aud=OUT/f"{jf.stem}_scene{i}_en.mp3"
   if not aud.exists(): raise FileNotFoundError(f"Missing narration: {aud}. Run generate_voice.py first.")
   mp=OUT/f"{jf.stem}_part{i}.mp4"
   subprocess.run(["ffmpeg","-y","-loop","1","-i",str(img),"-i",str(aud),"-c:v","libx264","-tune","stillimage","-c:a","aac","-b:a","128k","-shortest","-pix_fmt","yuv420p",str(mp)],check=True)
   parts.append(mp)
  concat=OUT/f"{jf.stem}_concat.txt"; concat.write_text("".join(f"file '{p.resolve()}'\\n" for p in parts))
  final=OUT/f"{jf.stem}.mp4"
  subprocess.run(["ffmpeg","-y","-f","concat","-safe","0","-i",str(concat),"-c","copy",str(final)],check=True)
  print("Rendered",final)
if __name__=="__main__": main()

