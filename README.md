# Doodle Dino Pals automation

This GitHub Actions workflow creates three short story scripts, generates English and Hindi
voiceovers, renders vertical MP4 videos, and uploads the generated files as a downloadable
GitHub Actions artifact.

## Scheduled run

The workflow runs every day at **09:00 India Standard Time (IST)**. You can also start it
manually from the repository's **Actions** tab by selecting **Daily Dino Shorts** and
clicking **Run workflow**.

## Run locally

Install Python dependencies:

```bash
python -m pip install -r requirements.txt
```

Install FFmpeg and make sure it is available on your PATH. Then run:

```bash
python daily_shorts.py
python generate_voice.py
python video_renderer.py
```

Generated scripts, audio, images, and MP4 files are saved in `output/`.

## Download generated videos

Open the completed run under **Actions**, then download the
`dino-shorts-output` artifact. Artifacts are retained for 7 days.

## Publishing

This workflow only generates videos and uploads them as GitHub Actions artifacts.
**YouTube uploading and publishing are disabled.**
