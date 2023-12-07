from gtts import gTTS

def text_to_speech(
        text,
        language,
        filename
    ):
    # Create a gTTS object
    tts = gTTS(
        text=text,
        lang=language,
        slow=False
    )

    # Save the converted audio to a file
    tts.save(filename)

text = input("Input text: ")
language = input("Input language(default is en): ").strip()
filename = input("Input filename(default output.mp3): ").strip()

language = 'en' if not language else language
filename = 'output.mp3' if not filename else filename

text_to_speech(text, language, filename)
