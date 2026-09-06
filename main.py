import speech_recognition as sr   
import webbrowser  # to open web borwser
import pyttsx3    # Text to speech
import MusicLibrary # Local file
import requests   # to open browser
from google import genai   # for gemini
from google.genai import types
from gtts import gTTS  # Text to speech better than pyttsx3
import pygame      # to speak the mp3 file
import time       
import os
from dotenv import load_dotenv  # to fetch api keys in .env file

load_dotenv("API_Keys.env")  # to load env file

#recognizer=sr.Recognizer()
engine=pyttsx3.init()
newsapi = os.getenv("NEWS_API_KEY")
url=f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}"

# def old_speak(text):
#     engine.say(text)
#     engine.runAndWait()

def speak(text):
    tts=gTTS(text)
    tts.save("temp.mp3")

    pygame.mixer.init()

    pygame.mixer.music.load("temp.mp3")
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        time.sleep(0.1)

    pygame.mixer.music.unload()   

def aiprocess(command):
    client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=command,
        config=types.GenerateContentConfig(
            system_instruction=(
                "You are Jarvis, a voice assistant. "
                "And skilled in general tasks and give short responses"
            ),
            automatic_function_calling=types.AutomaticFunctionCallingConfig(
                disable=True
            )
        )
    )

    return response.text    

def processing(c):
    print(c)
    if "open google" in c.lower():
        print("Openning...")
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
            print("Openning...")
            webbrowser.open("https://facebook.com")
    elif "open youtube" in c.lower():
            print("Openning...")
            webbrowser.open("https://youtube.com")
    elif c.lower().startswith("play"):
        song=c.lower().split(" ")[1]
        webbrowser.open(MusicLibrary.music[song])         
    elif "news" in c.lower():

        r = requests.get(
            f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}"
        )

        if r.status_code == 200:

            # Parse the JSON response
            data = r.json()

            # Extract the articles
            articles = data.get("articles", [])

            # Speak the headlines
            for article in articles:
                speak(article["title"])
    else:
        #let openAI handle the request   
        output=aiprocess(c)   
        print("AI Response:", output)    
        speak(output)   
             

if __name__=="__main__":
    speak("Initializing Jarvis......")

    while True:

        # obtain audio from the microphone
        r = sr.Recognizer()

        # recognize speech using Sphinx
        try:
            with sr.Microphone() as source:
                print("Say something!")
                audio = r.listen(source, timeout=2, phrase_time_limit=2)
            word=r.recognize_google(audio)
            print(word)

            if word.lower()=="jarvis":
                speak("Yeah")

                while True:

                    try:
                        with sr.Microphone() as source:
                            print("Listening....")
                            audio = r.listen(source, timeout=3, phrase_time_limit=3)
                            command=r.recognize_google(audio)
                            processing(command)
                        
                    except Exception as e:
                        print(e)    

        except Exception as e:
            print("Error; {0}".format(e))