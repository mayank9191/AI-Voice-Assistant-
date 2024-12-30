import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
import AI
import subprocess
import applications
import websites
import volume_using_gestures


recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "e21c35366ad6449095880c86a111f02b"


def speak(text):
    # Name: Microsoft David Desktop - English(United States) [0]

    # Name: Microsoft Zira Desktop - English(United States)  [1]
    rate = engine.getProperty('rate')
    voices = engine.getProperty('voices')
    engine.setProperty("voice", voices[1].id)
    engine.setProperty("rate", 150)
    engine.say(text)
    engine.runAndWait()


def processCommand(c):
    if (c.lower().split(" ")[1] in websites.requests.keys()):
        site = c.lower().split(" ")[1]
        link = websites.requests[site]
        webbrowser.open(link)

    elif (c.lower().startswith("play")):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music[song]
        webbrowser.open(link)

    elif ("news" in c.lower()):
        r = requests.get(
            f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        if r.status_code == 200:
            # Parse the JSON response
            data = r.json()

            # Extract the articles
            articles = data.get("articles", [])

            # print the headlines
            for article in articles:
                speak(article['title'])
    elif (c.lower().split(" ")[1] in applications.apps.keys()):
        app = c.lower().split(" ")[1]
        subprocess.Popen(applications.apps[app])

    elif ("volume gesture adjuster" in c.lower()):
        volume_using_gestures.volume_adjuster()

    else:
        # Let AI handle the request
        speak(AI.aiProcess(c))


if __name__ == "__main__":
    speak("Welcome sir, Jarvis  here.....")
    while True:
        # Listen for the wake word "Jarvis"
        # Obtain audio from the microphone

        r = sr.Recognizer()

        # recognize speech using google

        try:

            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source)
                print("Listening...")
                audio = r.listen(source, timeout=5, phrase_time_limit=1)
            word = r.recognize_google(audio)
            if (word.lower() == "jarvis"):
                speak("Yes sir, How may i help you?")
                # Listen for command
                print("Jarvis Active...")
                with sr.Microphone() as source:
                    recognizer.adjust_for_ambient_noise(source)
                    audio = r.listen(source)
                    command = r.recognize_google(audio)
                    processCommand(command)

        except Exception as e:
            print(f"Error;{e}")
