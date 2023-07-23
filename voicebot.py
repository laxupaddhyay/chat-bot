import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import random
import threading
import tkinter as tk
from tkinter import messagebox

# Check the platform
is_windows = os.name == 'nt'

# Initialize text-to-speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# Global variables
WAKE_WORD = "jarvis"  # Wake word to activate the program
COMMANDS = {
    'wikipedia': {'search': True},
    'youtube': {'url': "https://www.youtube.com"},
    'google': {'url': "https://www.google.com"},
    'stackoverflow': {'url': "https://stackoverflow.com"},
    'music': {},
    'time': {},
    'code': {},
    'conversation': {},
    'images': {'url': "https://www.pinterest.com/search/visual/search"}
}


def speak(audio):
    """Speak the given text using the text-to-speech engine"""
    engine.say(audio)
    engine.runAndWait()


def wish_me():
    """Greet the user based on the current time"""
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        greeting = "Good Morning!"
    elif 12 <= hour < 18:
        greeting = "Good Afternoon!"
    else:
        greeting = "Good Evening!"

    speak(f"{greeting} I am Jarvis. Please tell me how may I assist you.")


def listen():
    """Listen to the user's voice command"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        speak("I am listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except Exception as e:
        speak("Sorry, I didn't catch that. Could you please repeat?")
        return "None"

    return query.lower()


def search_wikipedia(query):
    """Search for the given query on Wikipedia"""
    speak('Searching Wikipedia...')
    query = query.replace("wikipedia", "")
    try:
        results = wikipedia.summary(query, sentences=2)
        speak("According to Wikipedia")
        print(results)
        speak(results)
    except wikipedia.exceptions.DisambiguationError as e:
        speak("Multiple results found. Please provide more specific query.")
    except wikipedia.exceptions.PageError as e:
        speak("Sorry, no results found for the given query.")


def open_website(url):
    """Open the given URL in a web browser"""
    webbrowser.open(url)


def play_music():
    """Play a random music file from the music directory"""
    music_dir = 'D:\\THERATTING\\MUSIC' if is_windows else '/path/to/music/directory'
    songs = os.listdir(music_dir)
    if len(songs) > 0:
        random.shuffle(songs)
        os.startfile(os.path.join(music_dir, songs[0])) if is_windows else os.system(f'xdg-open {os.path.join(music_dir, songs[0])}')
    else:
        speak("Sorry, I couldn't find any music in your library.")


def get_current_time():
    """Get the current time and speak it"""
    now = datetime.datetime.now()
    str_time = now.strftime("%H:%M:%S")
    str_date = now.strftime("%B %d, %Y")
    speak(f"Sir, the current time is {str_time} on {str_date}")


def open_code_editor():
    """Open the code editor"""
    code_path = "C:\\Users\\Haris\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe" if is_windows else "/usr/bin/code"
    os.startfile(code_path) if is_windows else os.system(code_path)


def respond_to_query(query):
    """Process and respond to the user's query"""
    if 'wikipedia' in query and COMMANDS['wikipedia']['search']:
        search_wikipedia(query)

    elif 'youtube' in query:
        open_website(COMMANDS['youtube']['url'])

    elif 'google' in query:
        open_website(COMMANDS['google']['url'])

    elif 'stackoverflow' in query:
        open_website(COMMANDS['stackoverflow']['url'])

    elif 'music' in query:
        play_music()

    elif 'time' in query:
        get_current_time()

    elif 'code' in query:
        open_code_editor()

    elif 'conversation' in query:
        speak("Thank you for talking with me!")

    elif 'images' in query and COMMANDS['images']['url']:
        open_website(COMMANDS['images']['url'])

    else:
        speak("I'm sorry, I didn't understand your command. Can you please repeat?")


def handle_query():
    """Process the user's query"""
    query = entry.get().lower()
    entry.delete(0, tk.END)
    respond_to_query(query)


def listen_command():
    """Listen to the user's voice command"""
    with sr.Microphone() as source:
        speak("I am listening...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
        entry.delete(0, tk.END)
        entry.insert(0, query.lower())
        handle_query()

    except Exception as e:
        speak("Sorry, I didn't catch that. Could you please repeat?")
        messagebox.showerror("Error", "Sorry, I didn't catch that. Could you please repeat?")


def activate_jarvis():
    """Activate Jarvis with the wake word"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        while True:
            audio = r.listen(source)

            try:
                command = r.recognize_google(audio).lower()
                print(f"Command: {command}")

                if WAKE_WORD in command:
                    label.config(text="Listening...")
                    listen_command()
                    break

            except sr.UnknownValueError:
                pass


def on_closing():
    """Handle closing of the GUI window"""
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()


if __name__ == "__main__":
    # Create GUI
    root = tk.Tk()
    root.title("Jarvis")
    root.geometry("400x300")

    # Create label
    label = tk.Label(root, text="Please tell me how may I assist you.")
    label.pack(pady=10)

    # Create entry box
    entry = tk.Entry(root, font=("Helvetica", 14))
    entry.pack(pady=10)

    # Create button
    button = tk.Button(root, text="Submit", command=handle_query)
    button.pack(pady=10)

    # Initialize speech recognition
    r = sr.Recognizer()

    def listen_thread():
        """Start a new thread to listen for voice commands"""
        threading.Thread(target=listen_command).start()

    def activate_jarvis_thread():
        """Start a new thread to activate Jarvis with the wake word"""
        threading.Thread(target=activate_jarvis).start()

    # Bind closing event
    root.protocol("WM_DELETE_WINDOW", on_closing)

    # Start Jarvis
    wish_me()
    label.config(text="Say the wake word to activate me.")
    activate_jarvis_thread()

    # Run the GUI main loop
    root.mainloop()
