# Doodle Dino Pals Kids — Daily bilingual Shorts

This workflow creates exactly 3 original 40-second children's learning Shorts packages each day:
- English + Hindi scene narration with timestamps
- Visual/animation prompts and on-screen text
- Safe music guidance, descriptions and hashtags
- Separate English and Hindi MP3 narration tracks (6 MP3s total)

## Schedule
Runs daily at 09:00 India time and can also be started manually from GitHub Actions.

## Run manually
1. Open the repository's **Actions** tab.
2. Select **Daily Doodle Dino Pals - 3 Bilingual Shorts**.
3. Select **Run workflow**.

## Get the files
Open the completed workflow run and download the artifact named
`doodle-dino-pals-3-bilingual-shorts`. Artifacts are retained for 14 days.

## Important limitations
- This creates scripts and voice tracks, not finished MP4 videos.
- It does not upload videos to YouTube.
- `edge-tts` uses Microsoft's online speech service; availability and terms can change.
- YouTube upload automation needs a separate YouTube Data API OAuth setup and user authorization.
- GitHub Actions free usage is subject to GitHub's current account limits.
