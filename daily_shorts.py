import json, random
from pathlib import Path
OUT=Path("output"); OUT.mkdir(exist_ok=True)
TOPICS=[
 ("Dino learns to share","A friendly dinosaur learns that sharing toys makes playtime happier."),
 ("Dino washes hands","A little dinosaur learns to wash hands before eating."),
 ("Dino helps a friend","A dinosaur helps a friend who fell and discovers kindness."),
]
def main():
 for idx,(title,story) in enumerate(TOPICS,1):
  scenes=[
   {"en":story,"hi":"एक प्यारा डायनासोर सीखता है कि दूसरों की मदद और चीज़ें बाँटना अच्छी बात है।"},
   {"en":"They try it together and everyone smiles.","hi":"वे मिलकर ऐसा करते हैं और सभी खुश हो जाते हैं।"},
   {"en":"Be kind, share, and learn every day!","hi":"दयालु बनें, बाँटें और हर दिन कुछ नया सीखें!"}
  ]
  data={"title":title,"description":story,"scenes":scenes}
  (OUT/f"short_{idx}.json").write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding="utf-8")
 print("Generated 3 short scripts in output/")
if __name__=="__main__": main()
