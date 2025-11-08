import pyttsx3
import speech_recognition as sr
import time
from datetime import datetime
import sys
from threading import Thread
from PyQt5.QtWidgets import QApplication
from luna_ui import AssistantUI 

 
from lunaAI import get_ai_response 
print("update")

# Variables
r = sr.Recognizer()
keywords = [("luna", 1.0), ("hey luna", 1.0)]
app = QApplication(sys.argv)
ui = AssistantUI()

def speak(text):
    engine = pyttsx3.init()
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[1].id)
    engine.setProperty("rate", 150)
    
    engine.say(text)
    engine.runAndWait()

def callback(recognizer, audio):
    try:
        speech_as_text = recognizer.recognize_sphinx(audio, keyword_entries=keywords)
        print("Detected:", speech_as_text)

        if "luna" in speech_as_text or "hey luna" in speech_as_text:
            ui.update_text("Yes, sir") 
            recognizer_main()
    except sr.UnknownValueError:
        ui.update_text("What the hell was that") 
        speak("What the hell was that")

def start_recognizer():
    print("Waiting for the keyword... luna or hey luna")
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)

    r.listen_in_background(sr.Microphone(), callback)  

def recognizer_main():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    try:
        data = r.recognize_google(audio).lower()
        print("You Said:", data)
        ui.update_text(data) 

        if "how are you" in data:
            speak("I am fine")
        elif "what are you" in data:
            speak("I'm your personal virtual assistant")   
        elif "what time is it right now" in data:
            current_time = datetime.now().strftime("%I:%M %p")
            speak(f"It's {current_time} right now")
        elif "hello" in data:
            speak("Hi there")
       
        else:
            ai_response = get_ai_response(data)
            ui.update_text(ai_response)
            speak(ai_response)
        
        
        

    except sr.UnknownValueError:
        print("I didn't understand that")
    except sr.RequestError:
        print("Error connecting to recognition service.")


thread = Thread(target=start_recognizer, daemon=True)
thread.start()


sys.exit(app.exec_())
