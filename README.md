# Doodle Dino Pals automation (rebuilt)

This starter workflow creates 3 short story scripts, generates English/Hindi Edge-TTS audio,
renders vertical MP4s, and uploads MP4s as a GitHub Actions artifact.

## Run locally
```bash
python -m pip install -r requirements.txt
python daily_shorts.py
python generate_voice.py
python video_renderer.py
```
Requires FFmpeg installed and available on PATH.

## GitHub
Upload/commit these files to the repository root. Then open Actions and run
**Daily Doodle Dino Pals Videos** manually. It also schedules daily at 09:00 IST.

## Scope
This produces downloadable MP4s; it does NOT publish to YouTube. YouTube publishing needs
OAuth credentials and a configured upload step. Do not put credentials in source code.
