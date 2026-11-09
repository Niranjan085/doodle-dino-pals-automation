import asyncio,json
from pathlib import Path
import edge_tts
OUT=Path("output")
VOICES={"en":"en-IN-NeerjaNeural","hi":"hi-IN-SwaraNeural"}
async def main():
 for f in sorted(OUT.glob("short_*.json")):
  d=json.loads(f.read_text(encoding="utf-8"))
  for n,s in enumerate(d["scenes"],1):
   for lang,voice in VOICES.items():
    target=OUT/f"{f.stem}_scene{n}_{lang}.mp3"
    await edge_tts.Communicate(s[lang],voice=voice).save(str(target))
    print("Created",target)
if __name__=="__main__": asyncio.run(main())
