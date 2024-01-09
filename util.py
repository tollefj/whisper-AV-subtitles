import time


def get_subs(prediction, add_line_number=True):
    subs = []
    for i, pred in enumerate(prediction):
        start, end = pred["timestamp"]
        text = pred["text"].strip()
        start = time.strftime("%H:%M:%S,000", time.gmtime(start))
        end = time.strftime("%H:%M:%S,000", time.gmtime(end))
        srt = f"{i+1}\n{start} --> {end}\n{text}\n\n"
        subs.append(srt)
    return subs
