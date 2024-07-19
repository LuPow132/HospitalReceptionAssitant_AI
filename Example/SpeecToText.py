import speech_recognition as sr

recognizer = sr.Recognizer()
mic = sr.Microphone()

class SpeechToText:
    def speech_to_text_thai():
        with mic as source:
            # Adjust the recognizer sensitivity to ambient noise
            recognizer.adjust_for_ambient_noise(source)
            print("Listening...")
            audio = recognizer.listen(source)

            try:
                # Using google speech recognition
                text = recognizer.recognize_google(audio, language='th-TH')
                print(text)
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand the audio")
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")

        def speech_to_text_eng():
            with mic as source:
                # Adjust the recognizer sensitivity to ambient noise
                recognizer.adjust_for_ambient_noise(source)
                print("Listening...")
                audio = recognizer.listen(source)

                try:
                    # Using google speech recognition
                    text = recognizer.recognize_google(audio, language='en-EN')
                    print(text)
                except sr.UnknownValueError:
                    print("Google Speech Recognition could not understand the audio")
                except sr.RequestError as e:
                    print(f"Could not request results from Google Speech Recognition service; {e}")

if __name__ == "__main__":
    while True:
        SpeechToText.speech_to_text_thai()
