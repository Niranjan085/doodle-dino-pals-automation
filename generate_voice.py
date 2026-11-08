#!/usr/bin/env python3
"""Create separate English and Hindi MP3 narration tracks for today's 3 Shorts."""
import asyncio
import json
from pathlib import Path
import edge_tts

OUT = Path("output")
EN_VOICE = "en-IN-NeerjaNeural"
HI_VOICE = "hi-IN-SwaraNeural"

async def save_voice(text, voice, path):
    last_error = None
    for attempt in range(3):
        try:
            communicate = edge_tts.Communicate(text=text, voice=voice, rate="+0%", volume="+0%")
            await asyncio.wait_for(communicate.save(str(path)), timeout=180)
            if path.exists() and path.stat().st_size > 1000:
                return
            raise RuntimeError("Voice file is empty or unexpectedly small")
        except Exception as exc:
            last_error = exc
            if path.exists():
                path.unlink()
            if attempt == 2:
                raise RuntimeError(f"Could not create {path.name}: {last_error}") from last_error
            await asyncio.sleep(3 * (attempt + 1))

async def main():
    scripts = sorted(OUT.glob("*_short_[123].json"))
    if len(scripts) != 3:
        raise RuntimeError(f"Expected exactly 3 Shorts JSON files, found {len(scripts)}")
    for file in scripts:
        data = json.loads(file.read_text(encoding="utf-8"))
        english = " ".join(scene["english"] for scene in data["scenes"])
        hindi = " ".join(scene["hindi"] for scene in data["scenes"])
        await save_voice(english, EN_VOICE, file.with_name(file.stem + "_en.mp3"))
        await save_voice(hindi, HI_VOICE, file.with_name(file.stem + "_hi.mp3"))
    audio_files = list(OUT.glob("*_short_[123]_[eh][ni]*.mp3"))
    en_files = list(OUT.glob("*_short_[123]_en.mp3"))
    hi_files = list(OUT.glob("*_short_[123]_hi.mp3"))
    if len(en_files) != 3 or len(hi_files) != 3:
        raise RuntimeError("Expected 3 English and 3 Hindi MP3 files")
    print("Created 6 voice tracks: 3 English + 3 Hindi.")

if __name__ == "__main__":
    asyncio.run(main())
