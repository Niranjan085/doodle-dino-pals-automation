VIDEO AUTOMATION SETUP

This bundle contains:
- .github/workflows/daily.yml (replace the existing workflow)
- generate_voice.py (replace the existing voice script)
- video_renderer.py (add this new file)
Keep your existing daily_shorts.py unchanged.

After committing these files, open the repository's Actions tab and run
'Daily Doodle Dino Pals Videos'. On success, download the artifact named
'doodle-dino-pals-daily-videos'. It contains three .mp4 videos in output/.

Videos are 9:16 vertical educational cards with a simple original dinosaur
face. Narration alternates English and Hindi by scene; both languages appear
on screen. No music is added, so there is no unlicensed music risk.

This creates videos but does not publish them to YouTube. Uploading requires
your own Google OAuth authorization. Never share passwords, OTPs, refresh
tokens, or client secrets in chat.
