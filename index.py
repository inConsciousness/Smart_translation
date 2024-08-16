import speech_recognition as sr  # Automatic Speech Recognition (ASR)
from googletrans import Translator, LANGUAGES  # Machine Translation (MT)
from gtts import gTTS  # Text-to-Speech (TTS) Synthesis
import os
from pydub import AudioSegment  # Audio processing
from pydub.playback import play  # Audio playback
from datetime import datetime  # Timestamping for file management

def speech_to_text(recognizer, audio):
    """Convert spoken language to text using Google's ASR."""
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand the audio.")
        return None
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return None

def translate_text(text, target_lang):
    """Translate text into the target language using Google's Machine Translation."""
    translator = Translator()
    translated_text = translator.translate(text, dest=target_lang).text
    print(f"Translated Text: {translated_text}")
    return translated_text

def text_to_speech(text, lang, filename):
    """Convert text to speech using Google's TTS and save as an MP3 file."""
    tts = gTTS(text=text, lang=lang)
    tts.save(filename)

def play_audio(file_path):
    """Play the audio file."""
    audio = AudioSegment.from_mp3(file_path)
    play(audio)

if __name__ == "__main__":
    recognizer = sr.Recognizer()  # Initialize the speech recognizer

    # Capture audio input from the microphone
    with sr.Microphone() as source:
        print("Please speak:")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    # Convert speech to text (ASR)
    text = speech_to_text(recognizer, audio)

    if text:
        print(f"Recognized Text: {text}")

        # Display available languages for translation (MT)
        print("Available target languages:")
        for lang_code, lang_name in LANGUAGES.items():
            print(f"{lang_code}: {lang_name}")

        target_lang = input("Enter the target language code: ")

        # Generate unique filenames using timestamps
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        input_filename = f"input_speech_{timestamp}.mp3"
        output_filename = f"translated_speech_{timestamp}.mp3"

        # Save the recorded speech as an MP3 file
        with open(input_filename, "wb") as f:
            f.write(audio.get_wav_data())
        print(f"Input speech saved as {input_filename}")

        # Translate the recognized text (MT)
        translated_text = translate_text(text, target_lang)

        # Convert the translated text to speech (TTS)
        text_to_speech(translated_text, target_lang, output_filename)
        print(f"Translated speech saved as {output_filename}")

        # Play the translated speech audio
        play_audio(output_filename)
        
