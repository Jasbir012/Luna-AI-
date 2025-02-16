import pyttsx3
import speech_recognition as sr
import time
from datetime import datetime
import tkinter as tk
from threading import Thread

# Variables
r = sr.Recognizer()
keywords = [("luna", 1.0), ("hey luna", 1.0)]

# GUI Setup
root = tk.Tk()
root.geometry("800x400")
root.title("Hello, I'm Luna")
root.configure(bg="#1e1e1e")

# Chatbox for Text Display
chatbox = tk.Text(root, font=("Arial", 12), height=20, width=50)
chatbox.pack(pady=10)
chatbox.insert(tk.END, "Luna: I'm listening...\n")

def add_to_chatbox(speaker, text):
    root.after(0, lambda: chatbox.insert(tk.END, f"{speaker}: {text}\n"))
    root.after(0, lambda: chatbox.see(tk.END))

# Functions
def speak(text):
    engine = pyttsx3.init()
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[1].id)
    engine.setProperty("rate", 150)
    
    add_to_chatbox("Luna", text)  
    engine.say(text)
    engine.runAndWait()

def callback(recognizer, audio):
    try:
        speech_as_text = recognizer.recognize_sphinx(audio, keyword_entries=keywords)
        print("Detected:", speech_as_text)
        add_to_chatbox("You", speech_as_text)

        if "luna" in speech_as_text or "hey luna" in speech_as_text:
            speak("Yes, sir")
            recognizer_main()  
    except sr.UnknownValueError:
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
        add_to_chatbox("You", data)

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
            speak("I'm sorry sir, I did not understand your request")

    except sr.UnknownValueError:
        add_to_chatbox("Luna", "I didn't understand that")
    except sr.RequestError:
        add_to_chatbox("Luna", "Error connecting to recognition service.")

# Run recognizer in a separate thread
thread = Thread(target=start_recognizer, daemon=True)
thread.start()

# Start GUI loop
root.mainloop()
