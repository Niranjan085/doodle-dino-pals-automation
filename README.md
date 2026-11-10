# Doodle Dino Pals — Daily Shorts Generator

This project creates **three original, bilingual English + Hindi, vertical 2D animated cartoon story videos** each day.

## What it does

1. Selects three gentle, child-friendly stories from the built-in story library.
2. Creates English and Hindi narration with Microsoft Edge text-to-speech voices.
3. Draws an original colorful 2D dinosaur cartoon, story props, moving background details, character bobbing/waving, and bilingual captions with Pillow.
4. Adds subtle camera movement and combines narration into native 4K vertical 2160 × 3840 MP4 videos at 30 FPS by default (set `DINO_QUALITY=1080p` for faster Full HD runs).
5. Runs software tests and checks that every video has valid picture, sound, dimensions, and duration.
6. Saves the videos and a validation report as a downloadable GitHub Actions artifact.

## Video quality

The GitHub Actions workflow renders native 4K (2160 × 3840, 9:16) by default. Set `DINO_QUALITY=1080p` for a faster Full HD render. 4K rendering takes more CPU time and storage.

## Daily schedule

GitHub Actions runs at **09:00 India Standard Time (IST)**. You can also start it manually from the repository's **Actions** tab by selecting **Daily Dino Shorts** and choosing **Run workflow**.

## Download your videos

After a successful run:
1. Open the [Daily Dino Shorts Actions page](https://github.com/Niranjan085/doodle-dino-pals-automation/actions/workflows/daily.yml).
2. Open the completed run.
3. Download the **dino-shorts-output** artifact.
4. Extract it to find the MP4 videos and `validation-report.json`.

Artifacts are retained for 7 days, so download anything you want to keep.

## Run locally

Install Python 3.11+, FFmpeg (including ffprobe), and the fonts Noto Sans Devanagari and DejaVu Sans.

```bash
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python daily_shorts.py
python generate_voice.py
python video_renderer.py
```

Generated scripts, narration, scene images, intermediate clips, MP4 files, and the validation report are saved in `output/`.

## Important publishing setting

**YouTube upload and publishing are not configured.** This workflow only creates videos and stores them as GitHub Actions artifacts. It does not publish anything to YouTube.
