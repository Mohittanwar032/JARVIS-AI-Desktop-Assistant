from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from google import genai

import os
import webbrowser
import threading
import subprocess
import urllib.parse


# ==========================================
# SETUP
# ==========================================

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("ERROR: GEMINI_API_KEY not found in .env")

client = genai.Client(api_key=api_key)

app = Flask(__name__)


# ==========================================
# HOME
# ==========================================

@app.route("/")
def home():
    return render_template("index.html")


# ==========================================
# LOCAL COMMANDS
# ==========================================

def execute_local_command(command):

    command = command.lower().strip()

    # Remove Jarvis from beginning
    command = command.replace("jarvis", "").strip()


       # ------------------------------------------
    # PLAY ANYTHING ON YOUTUBE
    # ------------------------------------------

    play_phrases = [
        "play ",
        "can you play ",
        "could you play ",
        "please play "
    ]

    play_request = False

    for phrase in play_phrases:
        if phrase in command:
            play_request = True
            break

    if play_request:

        search_query = command

        search_query = search_query.replace("jarvis", "")
        search_query = search_query.replace("can you", "")
        search_query = search_query.replace("could you", "")
        search_query = search_query.replace("please", "")
        search_query = search_query.replace("open youtube", "")
        search_query = search_query.replace("on youtube", "")
        search_query = search_query.replace("youtube", "")
        search_query = search_query.replace("play", "")

        search_query = search_query.strip()

        if search_query:

            encoded_query = urllib.parse.quote(search_query)

            url = (
                "https://www.youtube.com/results"
                "?search_query=" + encoded_query
            )

            webbrowser.open(url)

            return {
                "executed": True,
                "reply": "Playing " + search_query + " on YouTube."
            }


    # ------------------------------------------
    # OPEN YOUTUBE
    # ------------------------------------------

    if "open youtube" in command:

        webbrowser.open(
            "https://www.youtube.com"
        )

        return {
            "executed": True,
            "reply": "Opening YouTube."
        }


    # ------------------------------------------
    # OPEN GOOGLE
    # ------------------------------------------

    if "open google" in command:

        webbrowser.open(
            "https://www.google.com"
        )

        return {
            "executed": True,
            "reply": "Opening Google."
        }


    # ------------------------------------------
    # GOOGLE SEARCH
    # ------------------------------------------

    if command.startswith("search for "):

        search_query = command.replace(
            "search for ",
            "",
            1
        ).strip()

        if search_query:

            encoded_query = urllib.parse.quote(search_query)

            webbrowser.open(
                "https://www.google.com/search?q="
                + encoded_query
            )

            return {
                "executed": True,
                "reply": "Searching for " + search_query + "."
            }


    elif command.startswith("search "):

        search_query = command.replace(
            "search ",
            "",
            1
        ).strip()

        if search_query:

            encoded_query = urllib.parse.quote(search_query)

            webbrowser.open(
                "https://www.google.com/search?q="
                + encoded_query
            )

            return {
                "executed": True,
                "reply": "Searching for " + search_query + "."
            }


    # ------------------------------------------
    # OPEN CHATGPT
    # ------------------------------------------

    if (
        "open chatgpt" in command
        or "open chat gpt" in command
        or "open chat g p t" in command
    ):

        webbrowser.open(
            "https://chatgpt.com"
        )

        return {
            "executed": True,
            "reply": "Opening ChatGPT."
        }


    # ------------------------------------------
    # OPEN GITHUB
    # ------------------------------------------

    if "open github" in command:

        webbrowser.open(
            "https://github.com"
        )

        return {
            "executed": True,
            "reply": "Opening GitHub."
        }


    # ------------------------------------------
    # OPEN LINKEDIN
    # ------------------------------------------

    if "open linkedin" in command:

        webbrowser.open(
            "https://www.linkedin.com"
        )

        return {
            "executed": True,
            "reply": "Opening LinkedIn."
        }


    # ------------------------------------------
    # OPEN CALCULATOR
    # ------------------------------------------

    if "open calculator" in command:

        subprocess.Popen(
            ["calc.exe"]
        )

        return {
            "executed": True,
            "reply": "Opening calculator."
        }

        # ==========================================
    # CAMERA CONTROLS
    # ==========================================

    # TURN ON CAMERA
    if (
        "open camera" in command
        or "open my camera" in command
        or "turn on camera" in command
        or "turn on my camera" in command
        or "start camera" in command
        or "start my camera" in command
    ):

        os.system("start microsoft.windows.camera:")

        return {
            "executed": True,
            "reply": "Turning on your camera, Mohit."
        }


    # TURN OFF CAMERA
    if (
        "close camera" in command
        or "close my camera" in command
        or "turn off camera" in command
        or "turn off my camera" in command
        or "stop camera" in command
        or "stop my camera" in command
    ):

        os.system(
            'taskkill /F /IM WindowsCamera.exe >nul 2>&1'
        )

        return {
            "executed": True,
            "reply": "Turning off your camera, Mohit."
        }


    # ------------------------------------------
    # OPEN NOTEPAD
    # ------------------------------------------


    # ------------------------------------------
    # OPEN NOTEPAD
    # ------------------------------------------

    if "open notepad" in command:

        subprocess.Popen(
            ["notepad.exe"]
        )

        return {
            "executed": True,
            "reply": "Opening Notepad."
        }


    # ------------------------------------------
    # OPEN PAINT
    # ------------------------------------------

    if "open paint" in command:

        subprocess.Popen(
            ["mspaint.exe"]
        )

        return {
            "executed": True,
            "reply": "Opening Paint."
        }


    # ------------------------------------------
    # OPEN COMMAND PROMPT
    # ------------------------------------------

    if (
        "open command prompt" in command
        or "open cmd" in command
    ):

        subprocess.Popen(
            ["cmd.exe"]
        )

        return {
            "executed": True,
            "reply": "Opening Command Prompt."
        }


    # ------------------------------------------
    # NO LOCAL COMMAND FOUND
    # ------------------------------------------

    return {
        "executed": False
    }


# ==========================================
# COMMAND ROUTE
# ==========================================

@app.route("/command", methods=["POST"])
def handle_command():

    try:

        data = request.get_json()

        if not data:

            return jsonify({
                "status": "error",
                "reply": "I did not receive a command."
            })


        user_command = data.get(
            "command",
            ""
        ).strip()


        print("YOU:", user_command)


        if not user_command:

            return jsonify({
                "status": "error",
                "reply": "I could not hear a command."
            })


        # ======================================
        # FIRST CHECK LOCAL COMMANDS
        # ======================================

        local_result = execute_local_command(
            user_command
        )


        if local_result["executed"]:

            jarvis_reply = local_result["reply"]

            print(
                "LOCAL COMMAND:",
                jarvis_reply
            )

            return jsonify({
                "status": "success",
                "type": "local",
                "command": user_command,
                "reply": jarvis_reply
            })


        # ======================================
        # OTHERWISE USE GEMINI
        # ======================================

        print("Sending to Gemini...")


        response = client.models.generate_content(

           model="gemini-3.5-flash",

            contents=(
                "You are JARVIS, Mohit's personal AI assistant. "
                "Speak naturally and concisely. "
                "Use plain text only. "
                "Do not use markdown. "
                "Keep normal responses to one or two sentences. "
                "Mohit said: "
                + user_command
            )
        )


        jarvis_reply = response.text


        print(
            "JARVIS:",
            jarvis_reply
        )


        return jsonify({

            "status": "success",

            "type": "ai",

            "command": user_command,

            "reply": jarvis_reply
        })


    # ==========================================
    # ERROR HANDLING
    # ==========================================

    except Exception as error:

        print(
            "JARVIS ERROR:",
            error
        )


        error_text = str(error)


        # Gemini quota error

        if (
            "429" in error_text
            or "RESOURCE_EXHAUSTED" in error_text
        ):

            return jsonify({

                "status": "error",

                "reply":
                    "Mohit, my AI request limit has been reached. "
                    "Local commands are still available."

            })


        return jsonify({

            "status": "error",

            "reply":
                "Sorry Mohit, I encountered a system error."

        }), 500


# ==========================================
# AUTO OPEN JARVIS
# ==========================================

def open_jarvis():

    webbrowser.open(
        "http://127.0.0.1:5000"
    )


# ==========================================
# START JARVIS
# ==========================================

if __name__ == "__main__":

    print("\n==============================")
    print("        JARVIS ONLINE")
    print("==============================\n")


    threading.Timer(
        1.5,
        open_jarvis
    ).start()


    app.run(

        host="127.0.0.1",

        port=5000,

        debug=True,

        use_reloader=False
    )