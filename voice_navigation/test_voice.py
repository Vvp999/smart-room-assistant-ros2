import speech_recognition as sr

r = sr.Recognizer()

while True:

    with sr.Microphone(device_index=8) as source:

        print("\nSpeak now...")

        r.adjust_for_ambient_noise(source, duration=1)

        audio = r.listen(source)

    try:
        text = r.recognize_google(audio)

        print("You said:", text)

        if text.lower() == "exit":
            break

    except Exception as e:
        print("Error:", e)