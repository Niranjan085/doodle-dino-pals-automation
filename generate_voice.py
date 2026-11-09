import asyncio
import json
from pathlib import Path

import edge_tts

OUT = Path("output")
VOICES = {
    "en": "en-IN-NeerjaNeural",
    "hi": "hi-IN-SwaraNeural",
}


async def save_voice(text, voice, target):
    last_error = None
    for attempt in range(1, 4):
        try:
            target.unlink(missing_ok=True)
            communicate = edge_tts.Communicate(text, voice=voice)
            await asyncio.wait_for(communicate.save(str(target)), timeout=120)
            if not target.exists() or target.stat().st_size < 500:
                raise RuntimeError(f"Voice file is missing or unexpectedly small: {target}")
            print(f"Created {target} ({target.stat().st_size} bytes)")
            return
        except Exception as exc:
            last_error = exc
            print(f"Voice attempt {attempt}/3 failed for {target.name}: {exc}")
            if attempt < 3:
                await asyncio.sleep(attempt * 3)
    raise RuntimeError(f"Could not generate {target.name}") from last_error


async def main():
    scripts = sorted(OUT.glob("short_*.json"))
    if not scripts:
        raise FileNotFoundError("No story scripts found. Run daily_shorts.py first.")

    for script in scripts:
        data = json.loads(script.read_text(encoding="utf-8"))
        for scene_number, scene in enumerate(data.get("scenes", []), start=1):
            for language, voice in VOICES.items():
                narration = scene.get(language, "").strip()
                if not narration:
                    raise ValueError(f"Missing {language} narration in {script.name}, scene {scene_number}")
                target = OUT / f"{script.stem}_scene{scene_number}_{language}.mp3"
                await save_voice(narration, voice, target)


if __name__ == "__main__":
    asyncio.run(main())
