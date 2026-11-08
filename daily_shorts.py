
#!/usr/bin/env python3
"""
Doodle Dino Pals - Daily YouTube Shorts Content Generator
Creates one educational YouTube Shorts content package every day.
"""

import json
from datetime import date
from pathlib import Path

OUTPUT_DIR = Path("output")

TOPICS = [
    {
        "title": "Why Is the Sky Blue?",
        "hook": "Hey Dino Pals! Have you ever wondered why the sky is blue?",
        "fact": "Sunlight contains many colors. Air scatters blue light more than most other colors, making the sky look blue.",
        "lesson": "The sky looks blue because of the way sunlight travels through our atmosphere!",
        "visual": "A cute green dinosaur looking up at a bright blue sky."
    },
    {
        "title": "How Do Plants Make Food?",
        "hook": "Hello Dino Pals! Did you know plants make their own food?",
        "fact": "Plants use sunlight, water and carbon dioxide to make food through photosynthesis.",
        "lesson": "Plants are amazing little food factories powered by sunlight!",
        "visual": "A cute dinosaur watching a green plant grow in sunshine."
    },
    {
        "title": "Why Do We Have Day and Night?",
        "hook": "Hey Dino Pals! Why does the Sun disappear at night?",
        "fact": "Earth spins around its axis. The side facing the Sun has daytime, while the other side has nighttime.",
        "lesson": "Earth's rotation gives us day and night!",
        "visual": "A smiling dinosaur watching Earth rotate between day and night."
    },
    {
        "title": "How Do Bees Help Flowers?",
        "hook": "Hello Dino Pals! Why are bees so important?",
        "fact": "Bees carry pollen between flowers, helping many plants produce seeds and fruits.",
        "lesson": "Tiny bees do a very big job for nature!",
        "visual": "A friendly dinosaur watching bees visit colorful flowers."
    },
    {
        "title": "Why Is the Ocean Salty?",
        "hook": "Hey Dino Pals! Have you ever tasted ocean water?",
        "fact": "Rocks release dissolved minerals into rivers, which carry them to the ocean. This helps make seawater salty.",
        "lesson": "The ocean contains dissolved salts and minerals!",
        "visual": "A cute dinosaur standing beside a sparkling blue ocean."
    }
]


def generate_content():
    today = date.today()
    topic = TOPICS[today.toordinal() % len(TOPICS)]

    narration = (
        topic["hook"] + "\n\n"
        + topic["fact"] + "\n\n"
        + topic["lesson"] + "\n\n"
        + "Follow Doodle Dino Pals for more fun facts. Bye, Dino Pals!"
    )

    content = {
        "date": today.isoformat(),
        "channel": "Doodle Dino Pals",
        "format": "YouTube Shorts",
        "title": topic["title"],
        "duration_target": "30-45 seconds",
        "hook": topic["hook"],
        "narration": narration,
        "visual_prompt": topic["visual"],
        "lesson": topic["lesson"],
        "description": (
            topic["title"]
            + " | Learn something new with Doodle Dino Pals!"
        ),
        "hashtags": [
            "#DoodleDinoPals",
            "#EducationalShorts",
            "#FunFacts",
            "#Learning",
            "#YouTubeShorts"
        ],
        "status": "script_ready"
    }

    return content


def save_content(content):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    today = content["date"]
    json_file = OUTPUT_DIR / f"{today}.json"
    text_file = OUTPUT_DIR / f"{today}.md"

    json_file.write_text(
        json.dumps(content, indent=4, ensure_ascii=False),
        encoding="utf-8"
    )

    markdown = f"""# {content['title']}

**Channel:** {content['channel']}

**Date:** {today}

## Narration

{content['narration']}

## Visual idea

{content['visual_prompt']}

## Description

{content['description']}

## Hashtags

{' '.join(content['hashtags'])}

## Status

{content['status']}
"""

    text_file.write_text(markdown, encoding="utf-8")

    print("SUCCESS: Daily content generated!")
    print(f"Title: {content['title']}")
    print(f"JSON: {json_file}")
    print(f"Script: {text_file}")


if __name__ == "__main__":
    daily_content = generate_content()
    save_content(daily_content)

