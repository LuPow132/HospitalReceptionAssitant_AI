import speech_recognition as sr

def main():
    while True:
        recognize_speech_from_mic()

def recognize_speech_from_mic():
    # Initialize recognizer
    recognizer = sr.Recognizer()

    # Set up microphone
    with sr.Microphone() as source:
        print("Adjusting for ambient noise... Please wait.")
        recognizer.adjust_for_ambient_noise(source)  # Adjust based on the surrounding noise level

        print("Say something in Thai:")
        audio = recognizer.listen(source)  # Listen for speech

    try:
        # Use Google Web Speech API to recognize Thai speech (supports Thai)
        print("Recognizing speech...")
        text = recognizer.recognize_google(audio, language="th-TH")  # Thai language code
        print(f"You said: {text}")
    
    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio.")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")

if __name__ == "__main__":
    main()
