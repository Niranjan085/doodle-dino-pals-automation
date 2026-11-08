#!/usr/bin/env python3
"""Create exactly three bilingual, kid-safe Shorts packages for today."""
from datetime import date
from pathlib import Path
import json

OUT = Path("output")
OUT.mkdir(exist_ok=True)

TOPICS = [
    {
        "title": "Why Is the Sky Blue? | Aasman Neela Kyun Hai?",
        "topic": "Why the sky looks blue",
        "en": [
            "Wow! Why is the sky blue and not green?",
            "Sunlight has many colours mixed together.",
            "Tiny bits of air scatter blue light more than most other colours, so blue reaches our eyes from all directions.",
            "That is why our daytime sky looks blue. Science is amazing!",
        ],
        "hi": [
            "वाह! आसमान नीला क्यों दिखता है, हरा क्यों नहीं?",
            "सूरज की रोशनी में कई रंग मिले होते हैं।",
            "हवा के छोटे-छोटे कण नीली रोशनी को ज्यादा बिखेरते हैं, इसलिए नीली रोशनी हमें हर तरफ से दिखती है।",
            "इसीलिए दिन में आसमान नीला दिखता है। विज्ञान कमाल है!",
        ],
        "visuals": [
            "A cheerful cartoon dinosaur points up at a bright blue sky; big question mark pops in.",
            "A sunbeam with a rainbow spectrum streams toward Earth.",
            "Simple child-friendly animation: tiny air particles scatter blue rays in many directions.",
            "Dinosaur smiles; blue sky fills the frame; cheerful end card.",
        ],
        "screen": ["WHY BLUE?", "SUNLIGHT HAS MANY COLOURS", "AIR SCATTERS BLUE LIGHT", "SCIENCE IS AMAZING!"],
    },
    {
        "title": "How Do Plants Drink Water? | Paudhe Paani Kaise Peete Hain?",
        "topic": "How plants take in water",
        "en": [
            "Can a plant drink without a mouth? Yes!",
            "A plant takes in water through tiny roots under the soil.",
            "The water travels up the stem to the leaves. Leaves use water and sunlight to help make food.",
            "So give your plant a little water and lots of care!",
        ],
        "hi": [
            "क्या पौधा बिना मुँह के पानी पी सकता है? हाँ!",
            "पौधा मिट्टी के अंदर मौजूद छोटी जड़ों से पानी लेता है।",
            "पानी तने से होकर पत्तियों तक जाता है। पत्तियाँ पानी और धूप की मदद से भोजन बनाती हैं।",
            "अपने पौधे को सही मात्रा में पानी और ढेर सारा प्यार दें!",
        ],
        "visuals": [
            "Cute dinosaur looks at a thirsty potted plant; question bubble appears.",
            "Camera moves below soil to show tiny roots absorbing blue water droplets.",
            "Blue droplets travel up a transparent stem into green leaves; sunlight sparkles.",
            "Dinosaur gently waters plant; plant looks happy; end card.",
        ],
        "screen": ["PLANTS CAN DRINK!", "ROOTS TAKE IN WATER", "WATER TRAVELS TO LEAVES", "CARE FOR PLANTS"],
    },
    {
        "title": "Why Do We Have Five Fingers? | Hamari Paanch Ungliyan Kyun?",
        "topic": "How fingers help us",
        "en": [
            "Look at your hand! What can five fingers do?",
            "Our fingers help us hold, pick up, point, draw and make things.",
            "The thumb can touch the other fingers. This helps us grip objects carefully.",
            "Wiggle your fingers and try drawing a star!",
        ],
        "hi": [
            "अपने हाथ को देखो! पाँच उंगलियाँ क्या कर सकती हैं?",
            "हमारी उंगलियाँ चीज़ें पकड़ने, उठाने, इशारा करने और चित्र बनाने में मदद करती हैं।",
            "अंगूठा बाकी उंगलियों को छू सकता है। इससे हम चीज़ों को अच्छी तरह पकड़ पाते हैं।",
            "अपनी उंगलियाँ हिलाओ और एक तारा बनाकर देखो!",
        ],
        "visuals": [
            "Friendly cartoon dino holds up a hand; five fingers pop up one by one.",
            "Hand gently holds a crayon, a toy block and points to a star.",
            "Close-up animation of thumb touching each fingertip; simple labels.",
            "A childlike hand draws a star; dinosaur cheers; end card.",
        ],
        "screen": ["FIVE FINGERS!", "HOLD • PICK • DRAW", "THE THUMB HELPS US GRIP", "TRY DRAWING A STAR!"],
    },
    {
        "title": "Do Bees Help Flowers? | Madhumakkhiyan Phoolon Ki Madad?",
        "topic": "How bees help flowers",
        "en": [
            "Buzz, buzz! Tiny bees are super helpers!",
            "When a bee visits a flower for nectar, pollen can stick to its body.",
            "The bee carries pollen to another flower. This helps many plants make seeds and fruit.",
            "Bees are important. Watch them from a safe distance!",
        ],
        "hi": [
            "भन-भन! छोटी मधुमक्खियाँ बहुत मददगार होती हैं!",
            "जब मधुमक्खी रस लेने फूल पर बैठती है, तो पराग उसके शरीर से चिपक सकता है।",
            "मधुमक्खी पराग को दूसरे फूल तक ले जाती है। इससे पौधों को बीज और फल बनाने में मदद मिलती है।",
            "मधुमक्खियाँ बहुत जरूरी हैं। उन्हें सुरक्षित दूरी से देखें!",
        ],
        "visuals": [
            "Cute smiling bee flies toward a colourful flower; dino watches happily.",
            "Bee collects nectar; a few golden pollen dots stick to its fuzzy body.",
            "Bee visits a second flower; pollen dots transfer; fruit and seeds appear.",
            "Bee flies away; dinosaur waves from a safe distance; end card.",
        ],
        "screen": ["BEE HELPERS!", "POLLEN STICKS TO THE BEE", "POLLEN HELPS PLANTS", "WATCH BEES SAFELY"],
    },
    {
        "title": "Why Does the Moon Change Shape? | Chaand Ka Aakar Kyun Badalta Hai?",
        "topic": "Moon phases",
        "en": [
            "Is the Moon changing its shape? Not really!",
            "The Moon is round, and sunlight lights up half of it.",
            "As the Moon moves around Earth, we see different amounts of its bright half. These are Moon phases.",
            "Look up at the Moon with your family tonight!",
        ],
        "hi": [
            "क्या चाँद अपना आकार बदलता है? असल में नहीं!",
            "चाँद गोल है और सूरज की रोशनी उसके आधे हिस्से को चमकाती है।",
            "जब चाँद पृथ्वी के चारों ओर घूमता है, तो हमें उसका चमकता हिस्सा अलग-अलग दिखाई देता है। इन्हें चाँद की कलाएँ कहते हैं।",
            "आज रात परिवार के साथ चाँद को देखना!",
        ],
        "visuals": [
            "Dinosaur looks at a crescent Moon; question mark appears.",
            "A round Moon in space; sunlight illuminates one half.",
            "Simple orbit animation showing crescent, half and full Moon views.",
            "Dino and child look at Moon from a garden; end card.",
        ],
        "screen": ["MOON MAGIC!", "THE MOON IS ROUND", "WE SEE DIFFERENT LIT PARTS", "LOOK UP TONIGHT!"],
    },
    {
        "title": "Why Do We Wash Our Hands? | Haath Kyun Dhote Hain?",
        "topic": "Handwashing and hygiene",
        "en": [
            "Tiny germs can be hiding on our hands!",
            "We touch toys, doors and many other things every day.",
            "Soap and clean running water help wash germs and dirt away. Scrub all parts of your hands for about 20 seconds.",
            "Clean hands help keep us healthy. Great job!",
        ],
        "hi": [
            "हमारे हाथों पर छोटे-छोटे कीटाणु छिपे हो सकते हैं!",
            "हम रोज़ खिलौनों, दरवाज़ों और कई चीज़ों को छूते हैं।",
            "साबुन और साफ बहता पानी गंदगी और कीटाणुओं को हटाने में मदद करते हैं। हाथों के सभी हिस्सों को लगभग 20 सेकंड तक रगड़ें।",
            "साफ हाथ हमें स्वस्थ रखने में मदद करते हैं। शाबाश!",
        ],
        "visuals": [
            "Cute cartoon germs bounce on a child's hands; dino makes a surprised face.",
            "Child touches a toy, then a door handle; friendly icons appear.",
            "Hands lather with soap under running water; simple 20-second timer graphic.",
            "Sparkly clean hands give a thumbs-up; dino cheers; end card.",
        ],
        "screen": ["GERMS CAN HIDE!", "WE TOUCH MANY THINGS", "SOAP + WATER = CLEAN HANDS", "WASH FOR ABOUT 20 SECONDS"],
    },
    {
        "title": "How Do Birds Fly? | Pakshi Kaise Udte Hain?",
        "topic": "How birds fly",
        "en": [
            "Flap, flap! How can birds fly in the sky?",
            "Birds have wings and feathers that help them move through the air.",
            "Their strong chest muscles move the wings. Air moving around the wings helps create lift.",
            "Birds are amazing. Let's watch them without disturbing their nests!",
        ],
        "hi": [
            "फड़-फड़! पक्षी आसमान में कैसे उड़ते हैं?",
            "पक्षियों के पंख और पर उन्हें हवा में आगे बढ़ने में मदद करते हैं।",
            "उनकी मजबूत छाती की मांसपेशियाँ पंखों को चलाती हैं। पंखों के आसपास बहती हवा ऊपर उठने में मदद करती है।",
            "पक्षी कमाल के हैं। उनके घोंसलों को परेशान किए बिना उन्हें देखें!",
        ],
        "visuals": [
            "Happy cartoon bird flaps wings; dinosaur looks up in wonder.",
            "Close-up of feathers and wings; bird glides across a simple sky.",
            "Simple arrows show air moving around a wing; bird gently rises.",
            "Bird flies near trees while nest remains undisturbed; end card.",
        ],
        "screen": ["HOW DO BIRDS FLY?", "WINGS AND FEATHERS", "AIR HELPS CREATE LIFT", "RESPECT BIRD NESTS"],
    },
    {
        "title": "What Makes a Rainbow? | Indradhanush Kaise Banta Hai?",
        "topic": "How rainbows form",
        "en": [
            "A colourful rainbow in the sky? Wow!",
            "Sunlight may look white, but it contains many colours.",
            "When sunlight passes through tiny water drops, the light bends and spreads into different colours.",
            "Red, orange, yellow, green, blue and violet. Nature is beautiful!",
        ],
        "hi": [
            "आसमान में रंग-बिरंगा इंद्रधनुष? वाह!",
            "सूरज की रोशनी सफेद दिख सकती है, लेकिन उसमें कई रंग होते हैं।",
            "जब सूरज की रोशनी पानी की छोटी बूंदों से गुजरती है, तो वह मुड़कर अलग-अलग रंगों में बँट जाती है।",
            "लाल, नारंगी, पीला, हरा, नीला और बैंगनी। प्रकृति सुंदर है!",
        ],
        "visuals": [
            "Dinosaur spots a rainbow after rain; colourful sparkle animation.",
            "A white sunbeam shines toward a glassy water droplet.",
            "Light enters water droplets and emerges as a rainbow arc; clear simple diagram.",
            "Dino names rainbow colours with joyful gestures; end card.",
        ],
        "screen": ["RAINBOW MAGIC!", "SUNLIGHT HAS MANY COLOURS", "WATER DROPS SPLIT THE LIGHT", "COLOURS OF NATURE"],
    },
]

def main():
    day = date.today()
    # Rotate the topic pool so each day starts at a different topic.
    start = (day.toordinal() * 3) % len(TOPICS)
    chosen = [TOPICS[(start + i) % len(TOPICS)] for i in range(3)]
    index = {"date": day.isoformat(), "channel": "Doodle Dino Pals Kids", "shorts": []}
    for n, topic in enumerate(chosen, 1):
        scenes = []
        times = ["00:00-00:04", "00:04-00:12", "00:12-00:30", "00:30-00:40"]
        for i, t in enumerate(times):
            scenes.append({
                "time": t,
                "english": topic["en"][i],
                "hindi": topic["hi"][i],
                "visual_prompt": topic["visuals"][i],
                "on_screen_text": topic["screen"][i],
            })
        package = {
            "date": day.isoformat(),
            "number": n,
            "title": topic["title"],
            "topic": topic["topic"],
            "duration_seconds": 40,
            "hook": {"english": topic["en"][0], "hindi": topic["hi"][0]},
            "scenes": scenes,
            "music_guidance": "Use cheerful, gentle, child-friendly instrumental music from YouTube Audio Library or another properly licensed royalty-free source. Keep music low under narration; do not use copyrighted songs.",
            "description": f"Learn about {topic['topic']} with Doodle Dino Pals Kids! A fun, simple bilingual learning Short in English and Hindi. Made for curious kids and families.",
            "hashtags": ["#DoodleDinoPalsKids", "#KidsLearning", "#LearnWithFun", "#HindiEnglish", "#YouTubeShorts", "#ScienceForKids"],
            "safety_note": "Use original cartoon visuals. Avoid frightening imagery, unsafe challenges, or asking children to share personal information."
        }
        stem = f"{day.isoformat()}_short_{n}"
        (OUT / f"{stem}.json").write_text(json.dumps(package, ensure_ascii=False, indent=2), encoding="utf-8")
        md = [f"# Short {n}: {package['title']}", "", "**Duration:** 40 seconds", ""]
        for s in scenes:
            md += [f"## {s['time']}", f"- **English:** {s['english']}", f"- **Hindi:** {s['hindi']}", f"- **Visual:** {s['visual_prompt']}", f"- **On-screen text:** {s['on_screen_text']}", ""]
        md += ["**Music:** " + package["music_guidance"], "", "**Description:** " + package["description"], "", "**Hashtags:** " + " ".join(package["hashtags"])]
        (OUT / f"{stem}.md").write_text("\n".join(md), encoding="utf-8")
        index["shorts"].append({"number": n, "title": package["title"], "json": f"{stem}.json", "script": f"{stem}.md"})
    (OUT / f"{day.isoformat()}_index.json").write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Created exactly {len(chosen)} bilingual Shorts packages for {day.isoformat()}.")

if __name__ == "__main__":
    main()
