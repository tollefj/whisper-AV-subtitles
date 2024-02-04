import PySimpleGUI as sg

from transcription import transcribe
from translate_srt import translate
from utils.threading import ReturnValueThread

# if __name__ == "__main__":
#     fire.Fire(transcribe)
sg.theme("DarkGrey4")
sg.SetOptions(font=("Helvetica", 16))

whisper_models = [
    "base",
    "small",
    "medium",
    "NbAiLabBeta/nb-whisper-base",
    "NbAiLabBeta/nb-whisper-small",
    "NbAiLabBeta/nb-whisper-medium",
]
default_model = "NbAiLabBeta/nb-whisper-small"

sg_model_selector = sg.Combo(whisper_models, default_value=default_model, size=(40, 1))

layout = [
    [
        sg.Text("Select file/URL:", size=(15, 1)),
        sg.Input(size=(30, 1)),
        sg.FileBrowse(size=(10, 1)),
    ],
    [sg.Text("Select model:", size=(15, 1)), sg_model_selector],
    [sg.Button("Transcribe", size=(10, 1)), sg.Button("Exit", size=(10, 1))],
    [
        sg.Button("Translate: English", key="-TRANSLATE_EN-", disabled=True),
        sg.Button("Translate: Arabic", key="-TRANSLATE_AR-", disabled=True),
    ],
    [sg.Text("", key="-STATUS-", size=(55, 1))],
]

# DEFAULT_MODEL = "base"
DEFAULT_MODEL = "NbAiLabBeta/nb-whisper-small"


def transcribe_and_update_ui(
    window,
    media_path: str,
    model: str = DEFAULT_MODEL,
    align: bool = True,
    diarize: bool = False,
    delete_files: bool = False,
    skip_download: bool = False,
) -> None:
    store = transcribe(
        media_path=media_path,
        model=model,
        align=align,
        diarize=diarize,
        delete_files=delete_files,
        skip_download=skip_download,
    )
    window.write_event_value("-DONE-", "")
    return store


if __name__ == "__main__":
    window = sg.Window("Transcriber", layout)
    event, values = window.read()
    window["-STATUS-"].update("Select a file or URL to transcribe.")
    _thread = ReturnValueThread(
        target=transcribe_and_update_ui, args=(window, values[0], values[1])
    )

    while True:
        # event, values = window.read(timeout=500)
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == "Exit":
            break
        elif event == "Transcribe":
            window["-STATUS-"].update("Transcribing... Please wait")
            _thread.start()

        elif event == "-DONE-":
            window["-STATUS-"].update("Completed. Ready to transcribe.")
            window["-TRANSLATE_EN-"].update(disabled=False)
            window["-TRANSLATE_AR-"].update(disabled=False)

        if event in ["-TRANSLATE_EN-", "-TRANSLATE_AR-"]:
            language = "english" if event == "-TRANSLATE_EN-" else "arabic"
            result = _thread.join()
            srt_path = result["srt"]
            if srt_path:
                # use the translation thread
                _translate_thread = ReturnValueThread(
                    target=translate, args=(srt_path, language)
                )
                _translate_thread.start()

                window["-STATUS-"].update(f"Translating to {language}.. Please wait")
            else:
                window["-STATUS-"].update("Transcribe before translating.")
            window["-TRANSLATE_EN-"].update(disabled=True)
            window["-TRANSLATE_AR-"].update(disabled=True)

    window.close()
