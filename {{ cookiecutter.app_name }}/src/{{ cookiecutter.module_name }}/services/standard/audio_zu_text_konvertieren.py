import whisper

def audio_zu_text_konvertieren(audio_dateipfad):
    # wenn verwendet wir muss openai-whisper installiert sein
    import whisper

    model = whisper.load_model("base")
    result = model.transcribe(audio_dateipfad)
    return result["text"]