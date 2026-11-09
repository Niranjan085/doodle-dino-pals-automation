import json
from datetime import datetime, timezone
from pathlib import Path

OUT = Path("output")

# Original, gentle stories written for a young audience.
STORY_BANK = [
    {
        "title": "Dino Learns to Share",
        "description": "Dino discovers that sharing makes playtime more fun for everyone.",
        "scenes": [
            ("Dino has a colourful box of building blocks.", "डिनो के पास रंग-बिरंगे ब्लॉक्स का एक डिब्बा है।"),
            ("A friend wants to build too, so Dino shares the blocks.", "एक दोस्त भी खेलना चाहता है, इसलिए डिनो ब्लॉक्स बाँटता है।"),
            ("They build a tall tower together. Sharing is caring!", "दोनों मिलकर एक ऊँचा टावर बनाते हैं। बाँटना अच्छी बात है!"),
        ],
    },
    {
        "title": "Dino Washes Hands",
        "description": "Dino learns a simple hand-washing habit before snack time.",
        "scenes": [
            ("Dino is ready for a tasty snack.", "डिनो स्वादिष्ट नाश्ता खाने के लिए तैयार है।"),
            ("First, Dino washes both hands with soap and clean water.", "पहले डिनो साबुन और साफ पानी से दोनों हाथ धोता है।"),
            ("Now it is snack time. Clean hands help us stay healthy!", "अब नाश्ते का समय है। साफ हाथ हमें स्वस्थ रहने में मदद करते हैं!"),
        ],
    },
    {
        "title": "Dino Helps a Friend",
        "description": "Dino learns that a small act of kindness can brighten someone's day.",
        "scenes": [
            ("Dino sees a friend having trouble carrying some books.", "डिनो देखता है कि एक दोस्त को किताबें उठाने में परेशानी हो रही है।"),
            ("Dino asks, 'Would you like some help?'", "डिनो पूछता है, 'क्या मैं तुम्हारी मदद करूँ?'"),
            ("They carry the books together. Helping feels great!", "दोनों मिलकर किताबें उठाते हैं। मदद करना अच्छा लगता है!"),
        ],
    },
    {
        "title": "Dino Learns About Plants",
        "description": "Dino discovers how a little care helps a plant grow.",
        "scenes": [
            ("Dino finds a tiny green plant in the garden.", "डिनो को बगीचे में एक नन्हा हरा पौधा मिलता है।"),
            ("Dino gives the plant water and makes sure it gets sunlight.", "डिनो पौधे को पानी देता है और धूप मिलने देता है।"),
            ("With care and time, the plant grows. Nature is amazing!", "देखभाल और समय से पौधा बढ़ता है। प्रकृति अद्भुत है!"),
        ],
    },
    {
        "title": "Dino Tidies Up",
        "description": "Dino learns to put toys away after playtime.",
        "scenes": [
            ("Playtime is over and toys are all around the room.", "खेल खत्म हो गया है और कमरे में खिलौने बिखरे हैं।"),
            ("Dino puts each toy back in its own place.", "डिनो हर खिलौने को उसकी सही जगह पर रखता है।"),
            ("The room looks neat. Tidying up is a helpful habit!", "कमरा साफ-सुथरा दिखता है। सफाई रखना अच्छी आदत है!"),
        ],
    },
    {
        "title": "Dino Tries Something New",
        "description": "Dino learns that practice helps us improve at new things.",
        "scenes": [
            ("Dino wants to learn how to draw a star.", "डिनो एक तारा बनाना सीखना चाहता है।"),
            ("The first star looks funny, but Dino keeps practising.", "पहला तारा थोड़ा अजीब बनता है, लेकिन डिनो अभ्यास करता रहता है।"),
            ("Dino draws a lovely star. Every try helps us learn!", "डिनो एक सुंदर तारा बनाता है। हर कोशिश हमें कुछ सिखाती है!"),
        ],
    },
]


def build_story(story):
    return {
        "title": story["title"],
        "description": story["description"],
        "language": ["en", "hi"],
        "scenes": [
            {"en": en, "hi": hi}
            for en, hi in story["scenes"]
        ],
    }


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    # Rotate the story set by date so consecutive daily runs do not repeat
    # the same three stories immediately.
    day_number = datetime.now(timezone.utc).date().toordinal()
    start = day_number % len(STORY_BANK)
    selected = [STORY_BANK[(start + offset) % len(STORY_BANK)] for offset in range(3)]

    for index, story in enumerate(selected, start=1):
        data = build_story(story)
        if len(data["scenes"]) != 3 or any(not s["en"] or not s["hi"] for s in data["scenes"]):
            raise ValueError(f"Invalid bilingual story: {story['title']}")
        target = OUT / f"short_{index}.json"
        target.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Created {target}: {story['title']}")

    print("Generated 3 original bilingual story scripts.")


if __name__ == "__main__":
    main()
