import pyttsx3

def convert_text_to_speech(text: str, output_path: str) -> str:
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    male_voice = None
    for voice in voices:
        if "male" in voice.name.lower():
            male_voice = voice
            break
    if male_voice:
        engine.setProperty('voice', male_voice.id)
    else:
        engine.setProperty('voice', voices[0].id)
    
    engine.save_to_file(text, output_path)
    engine.runAndWait()
    return output_path
