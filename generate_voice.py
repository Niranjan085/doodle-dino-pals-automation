import asyncio, json
from pathlib import Path
import edge_tts

OUT = Path("output")
VOICES = {"en": "en-IN-NeerjaNeural", "hi": "hi-IN-SwaraNeural"}

async def speak(text, voice, path):
    last = None
    for attempt in range(3):
        try:
            await edge_tts.Communicate(text=text, voice=voice).save(str(path))
            if path.exists() and path.stat().st_size > 1000:
                return
        except Exception as exc:
            last = exc
        await asyncio.sleep(2 * (attempt + 1))
    raise RuntimeError(f"Could not create {path.name}: {last}")

async def main():
    files = sorted(OUT.glob("*_short_[123].json"))
    if len(files) != 3:
        raise RuntimeError(f"Expected 3 script files, found {len(files)}")
    for f in files:
        data = json.loads(f.read_text(encoding="utf-8"))
        for i, scene in enumerate(data["scenes"]):
            lang = "en" if i % 2 == 0 else "hi"
            await speak(scene[lang], VOICES[lang],
                        f.with_name(f.stem + f"_scene{i+1}.mp3"))
    print("Created 12 scene voice clips.")
if __name__ == "__main__":
    asyncio.run(main())
