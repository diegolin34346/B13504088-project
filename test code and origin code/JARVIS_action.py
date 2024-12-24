import pyttsx3
import speech_recognition as sr
import os
import webbrowser

engine = pyttsx3.init() #initializing the engine
voices = engine.getProperty('voices') #getting details of current voice

def speak(text,voice=0):
    engine.setProperty('voice', voices[voice].id) #changing the voice, 0 for English, 1 for Chinese
    engine.say(text) # sending the text to the engine
    print(text) # printing the text
    engine.runAndWait() #running the engine


def listen():
    recognizer = sr.Recognizer() #  Create a recognizer instance
    with sr.Microphone() as source:
        print("Listening...")
        try: # Try to recognize the audio input
            audio = recognizer.listen(source) # Listen for audio input
            text = recognizer.recognize_google(audio, language="zh-TW,en")  
            print(f"Recognized text: {text}")      
            return text            
        except sr.UnknownValueError: # If the audio input is not recognized
            print("Sorry, I could not understand the audio.")
            return None
        except sr.RequestError as e: # If there is an error 
            print(f"Error with the speech recognition service: {e}")
            return None

def take_action(command):
    """Perform actions based on the command."""
    if "Open Google" in command:
        speak("opening Google")
        webbrowser.open("https://www.google.com")
    elif "What is your name" in command:
        speak("I am your personal assistant, JARVIS.")
    elif "exit" in command or "quit" in command or "bye" in command:
        speak("Goodbye!")
        exit()
    else:
        speak("Sorry, I can't do that yet.")

# Main Loop
speak("Hello! How can I assist you?")
while True:
    command = listen()
    if command:
        take_action(command)
