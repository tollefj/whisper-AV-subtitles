import srt
from tqdm import tqdm
from transformers import pipeline

models = {
    "english": "Helsinki-NLP/opus-mt-gmq-en",
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
    batch_size = 16
    for batch in tqdm(range(0, len(prefixed), batch_size)):
        translated = pipe(prefixed[batch : batch + batch_size])
        translated_sub.extend([t["translation_text"] for t in translated])

    # update the content of the subtitles:
    for i in range(len(subs)):
        subs[i].content = translated_sub[i]
    print(translated_sub[:5])
    print(subs[:5])

    new_path = path.replace(".srt", f"_{language}.srt")
    with open(new_path, "w", encoding="utf-8") as f:
        f.write(srt.compose(subs))
    print(f"The translated subtitles are saved to {new_path}")


if __name__ == "__main__":
    tmp_path = "store/watch?v=nyxcO2vdcCg/subtitles.srt"
    translate(tmp_path, "english")
