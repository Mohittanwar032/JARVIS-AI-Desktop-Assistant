import webbrowser
import subprocess
import os
import pyttsx3
import pywhatkit
import speech_recognition as sr

from dotenv import load_dotenv
from google import genai


# ==========================================
# GEMINI SETUP
# ==========================================

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)


# ==========================================
# JARVIS SPEAK
# ==========================================

def speak(text):

    text = str(text)

    print("JARVIS:", text)

    # Remove markdown symbols from Gemini response
    clean_text = text.replace("*", "")
    clean_text = clean_text.replace("#", "")
    clean_text = clean_text.replace("`", "")

    # Create fresh voice engine
    engine = pyttsx3.init()

    engine.setProperty("rate", 175)

    engine.say(clean_text)
    engine.runAndWait()

    engine.stop()


# ==========================================
# JARVIS LISTEN
# ==========================================

def listen():

    recognizer = sr.Recognizer()

    with sr.Microphone() as source:

        print("Listening...")

        recognizer.adjust_for_ambient_noise(
            source,
            duration=1
        )

        try:

            audio = recognizer.listen(
                source,
                timeout=5,
                phrase_time_limit=10
            )

        except sr.WaitTimeoutError:
            return ""

    try:

        command = recognizer.recognize_google(audio)

        print("YOU:", command)

        return command

    except sr.UnknownValueError:

        return ""

    except sr.RequestError:

        speak("Speech recognition service is unavailable.")

        return ""


# ==========================================
# ASK GEMINI
# ==========================================

def ask_jarvis(question):

    try:

        response = client.models.generate_content(

            model="gemini-2.5-flash",

            contents=(
                "You are Jarvis, Mohit's personal AI assistant. "
                "Answer in plain text without markdown. "
                "Give short and clear spoken answers. "
                "Keep most answers under three sentences. "
                "User question: " + question
            )
        )

        return response.text

    except Exception as error:

        print("Gemini Error:", error)

        return "Sorry Mohit, I am having trouble connecting to my AI system."


# ==========================================
# EXECUTE COMMAND
# ==========================================

def execute_command(command):

    command = command.lower()


    # ======================================
    # PLAY SOMETHING ON YOUTUBE
    # ======================================

    if "youtube" in command and "play" in command:

        search_query = command

        # Remove command words
        search_query = search_query.replace("jarvis", "")
        search_query = search_query.replace("open youtube", "")
        search_query = search_query.replace("youtube", "")
        search_query = search_query.replace("and play", "")
        search_query = search_query.replace("play", "")
        search_query = search_query.replace("on", "")

        search_query = search_query.strip()

        if search_query:

            speak(
                "Playing " + search_query + " on YouTube."
            )

            pywhatkit.playonyt(search_query)

        return True


    # ======================================
    # PLAY DIRECTLY ON YOUTUBE
    # ======================================

    elif command.startswith("jarvis play") or command.startswith("play"):

        search_query = command

        search_query = search_query.replace("jarvis", "")
        search_query = search_query.replace("play", "")
        search_query = search_query.replace("on youtube", "")

        search_query = search_query.strip()

        if search_query:

            speak(
                "Playing " + search_query + " on YouTube."
            )

            pywhatkit.playonyt(search_query)

        return True


    # ======================================
    # OPEN YOUTUBE
    # ======================================

    elif "open youtube" in command:

        speak("Opening YouTube.")

        webbrowser.open(
            "https://www.youtube.com"
        )

        return True


    # ======================================
    # GOOGLE SEARCH
    # ======================================

    elif "search" in command:

        search_query = command

        search_query = search_query.replace("jarvis", "")
        search_query = search_query.replace("search google for", "")
        search_query = search_query.replace("search for", "")
        search_query = search_query.replace("search", "")

        search_query = search_query.strip()

        if search_query:

            speak(
                "Searching Google for " + search_query
            )

            url = (
                "https://www.google.com/search?q="
                + search_query.replace(" ", "+")
            )

            webbrowser.open(url)

        return True


    # ======================================
    # OPEN GOOGLE
    # ======================================

    elif "open google" in command:

        speak("Opening Google.")

        webbrowser.open(
            "https://www.google.com"
        )

        return True


    # ======================================
    # OPEN CHATGPT
    # ======================================

    elif "open chatgpt" in command or "open chat g p t" in command:

        speak("Opening ChatGPT.")

        webbrowser.open(
            "https://chatgpt.com"
        )

        return True


    # ======================================
    # OPEN GITHUB
    # ======================================

    elif "open github" in command:

        speak("Opening GitHub.")

        webbrowser.open(
            "https://github.com"
        )

        return True


    # ======================================
    # OPEN LINKEDIN
    # ======================================

    elif "open linkedin" in command:

        speak("Opening LinkedIn.")

        webbrowser.open(
            "https://www.linkedin.com"
        )

        return True


    # ======================================
    # OPEN CALCULATOR
    # ======================================

    elif "open calculator" in command:

        speak("Opening Calculator.")

        subprocess.Popen("calc.exe")

        return True


    # ======================================
    # OPEN NOTEPAD
    # ======================================

    elif "open notepad" in command:

        speak("Opening Notepad.")

        subprocess.Popen("notepad.exe")

        return True


    # ======================================
    # OPEN PAINT
    # ======================================

    elif "open paint" in command:

        speak("Opening Paint.")

        subprocess.Popen("mspaint.exe")

        return True


    # ======================================
    # OPEN COMMAND PROMPT
    # ======================================

    elif "open command prompt" in command:

        speak("Opening Command Prompt.")

        subprocess.Popen("cmd.exe")

        return True


    # No laptop command found
    return False


# ==========================================
# START JARVIS
# ==========================================

speak("Hello Mohit. Jarvis is online.")


# ==========================================
# CONTINUOUS MODE
# ==========================================

while True:

    command = listen()

    # Nothing heard
    if not command:
        continue


    command_lower = command.lower()


    # ======================================
    # STOP JARVIS
    # ======================================

    if (
        "jarvis stop" in command_lower
        or "stop jarvis" in command_lower
        or "jarvis exit" in command_lower
    ):

        speak("Goodbye Mohit.")

        break


    # ======================================
    # CHECK LAPTOP COMMAND
    # ======================================

    command_executed = execute_command(command)


    # ======================================
    # OTHERWISE ASK GEMINI
    # ======================================

    if not command_executed:

        print("Thinking...")

        answer = ask_jarvis(command)

        speak(answer)