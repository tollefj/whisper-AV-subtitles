import srt
from tqdm import tqdm
from transformers import pipeline

models = {
    "english": "Helsinki-NLP/opus-mt-en-gmq",
    "arabic": "Helsinki-NLP/opus-mt-tc-big-gmq-ar",
}

prefixes = {
    "english": ">>eng<<",
    "arabic": ">>ara<<",
}


def translate(path, language="english"):
    pipe = pipeline("translation", model=models[language])

    with open(path, "r", encoding="utf-8") as f:
        data = f.read()
    subs = list(srt.parse(data))
    prefixed = [f"{prefixes[language]} {sub.content}" for sub in subs]
    translated_sub = []
    batch_size = 32
    for batch in tqdm(range(0, len(prefixed), batch_size)):
        translated = pipe(prefixed[batch : batch + batch_size])
        translated_sub.extend([t["translation_text"] for t in translated])

    # update the content of the subtitles:
    for i, sub in enumerate(subs):
        sub.content = translated_sub[i]

    # write srt:
    new_path = path.replace(".srt", "_translated.srt")
    with open(new_path, "w", encoding="utf-8") as f:
        f.write(srt.compose(subs))
