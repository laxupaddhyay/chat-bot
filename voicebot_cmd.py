import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import random

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
    music_dir = 'D:\\THERATTING\\MUSIC' if os.name == 'nt' else '/path/to/music/directory'
    songs = os.listdir(music_dir)
    if len(songs) > 0:
        random.shuffle(songs)
        os.startfile(os.path.join(music_dir, songs[0])) if os.name == 'nt' else os.system(f'xdg-open {os.path.join(music_dir, songs[0])}')
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
    code_path = "C:\\Users\\Haris\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe" if os.name == 'nt' else "/usr/bin/code"
    os.startfile(code_path) if os.name == 'nt' else os.system(code_path)


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


if __name__ == "__main__":
    # Start Jarvis
    wish_me()
    while True:
        query = listen()
        if query != "None":
            respond_to_query(query)
