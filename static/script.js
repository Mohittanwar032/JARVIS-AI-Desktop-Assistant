// ==========================================================
// JARVIS // CONTINUOUS VOICE SYSTEM
// ==========================================================

const button = document.getElementById("micButton");
const statusText = document.getElementById("statusText");
const message = document.getElementById("jarvisMessage");

const SpeechRecognition =
    window.SpeechRecognition ||
    window.webkitSpeechRecognition;


// ==========================================================
// VARIABLES
// ==========================================================

let recognition;

let recognitionActive = false;
let jarvisActivated = false;
let jarvisSpeaking = false;
let processingCommand = false;


// ==========================================================
// HUD STATE
// ==========================================================

function setJarvisState(state) {

    document.body.classList.remove(
        "state-ready",
        "state-listening",
        "state-thinking",
        "state-speaking",
        "state-executing",
        "state-error"
    );

    document.body.classList.add(
        "state-" + state.toLowerCase()
    );

    statusText.innerText = state;
}


// ==========================================================
// TERMINAL LOG
// ==========================================================

function addTerminalLine(type, text) {

    const conversation =
        document.getElementById("conversation");

    if (!conversation) {
        return;
    }

    const line =
        document.createElement("p");

    const label =
        document.createElement("span");


    if (type === "YOU") {

        label.className = "sys";

        label.innerText =
            "YOU // ";

    } else {

        label.className = "ai";

        label.innerText =
            "JARVIS // ";
    }


    line.appendChild(label);

    line.appendChild(
        document.createTextNode(text)
    );

    conversation.appendChild(line);


    conversation.scrollTop =
        conversation.scrollHeight;
}


// ==========================================================
// START LISTENING
// ==========================================================

function startListening() {

    if (!jarvisActivated) {
        return;
    }


    if (jarvisSpeaking) {
        return;
    }


    if (processingCommand) {
        return;
    }


    if (recognitionActive) {
        return;
    }


    try {

        console.log(
            "Starting microphone..."
        );


        setJarvisState(
            "LISTENING"
        );


        message.innerText =
            "VOICE CHANNEL OPEN // Listening, Mohit...";


        button.innerHTML =
            '<span class="mic-symbol">◉</span> JARVIS ACTIVE';


        recognition.start();

    }

    catch (error) {

        console.log(
            "Microphone start error:",
            error
        );
    }
}


// ==========================================================
// STOP JARVIS
// ==========================================================

function stopJarvis() {

    console.log(
        "JARVIS going offline"
    );


    jarvisActivated = false;

    processingCommand = false;


    // Stop speech

    window.speechSynthesis.cancel();


    // Stop microphone

    if (recognitionActive) {

        try {

            recognition.stop();

        }

        catch (error) {

            console.log(
                "Recognition stop error:",
                error
            );
        }
    }


    setJarvisState(
        "READY"
    );


    message.innerText =
        "VOICE LINK CLOSED // JARVIS standing by.";


    button.innerHTML =
        '<span class="mic-symbol">◉</span> INITIATE VOICE LINK';
}


// ==========================================================
// SPEAK
// ==========================================================

function speak(text) {

    console.log(
        "JARVIS SPEAKING:",
        text
    );


    // ------------------------------------------------------
    // Stop microphone before JARVIS talks
    // ------------------------------------------------------

    if (recognitionActive) {

        try {

            recognition.stop();

        }

        catch (error) {

            console.log(
                "Could not stop microphone:",
                error
            );
        }
    }


    // Stop old speech

    window.speechSynthesis.cancel();


    const speech =
        new SpeechSynthesisUtterance(text);


    speech.volume = 1;

    // Slightly slower/deeper voice

    speech.rate = 0.95;

    speech.pitch = 0.82;


    // ------------------------------------------------------
    // SELECT VOICE
    // ------------------------------------------------------

    const voices =
        window.speechSynthesis.getVoices();


    const preferredVoice =

        voices.find(
            voice =>
                voice.name
                    .toLowerCase()
                    .includes("david")
        )

        ||

        voices.find(
            voice =>
                voice.name
                    .toLowerCase()
                    .includes("mark")
        )

        ||

        voices.find(
            voice =>
                voice.lang === "en-GB"
        )

        ||

        voices.find(
            voice =>
                voice.lang === "en-IN"
        )

        ||

        voices.find(
            voice =>
                voice.lang === "en-US"
        );


    if (preferredVoice) {

        speech.voice =
            preferredVoice;
    }


    // ======================================================
    // SPEAKING START
    // ======================================================

    speech.onstart = function () {

        console.log(
            "JARVIS voice started"
        );


        jarvisSpeaking = true;


        setJarvisState(
            "SPEAKING"
        );


        button.innerHTML =
            '<span class="mic-symbol">◉</span> VOICE OUTPUT ACTIVE';
    };


    // ======================================================
    // SPEAKING FINISHED
    // ======================================================

    speech.onend = function () {

        console.log(
            "JARVIS voice finished"
        );


        jarvisSpeaking = false;

        processingCommand = false;


        // --------------------------------------------------
        // Automatically listen again
        // --------------------------------------------------

        if (jarvisActivated) {

            setTimeout(
                function () {

                    startListening();

                },
                700
            );

        } else {

            setJarvisState(
                "READY"
            );


            button.innerHTML =
                '<span class="mic-symbol">◉</span> INITIATE VOICE LINK';
        }
    };


    // ======================================================
    // SPEECH ERROR
    // ======================================================

    speech.onerror = function (event) {

        console.error(
            "Speech synthesis error:",
            event
        );


        jarvisSpeaking = false;

        processingCommand = false;


        setJarvisState(
            "ERROR"
        );


        message.innerText =
            "VOICE OUTPUT ERROR";


        if (jarvisActivated) {

            setTimeout(
                function () {

                    startListening();

                },
                1000
            );
        }
    };


    // ======================================================
    // START SPEAKING
    // ======================================================

    window.speechSynthesis.speak(
        speech
    );
}


// ==========================================================
// SPEECH RECOGNITION SUPPORT
// ==========================================================

if (!SpeechRecognition) {

    setJarvisState(
        "ERROR"
    );


    statusText.innerText =
        "VOICE MODULE OFFLINE";


    message.innerText =
        "Speech recognition is not supported by this browser.";


    button.disabled = true;

}


// ==========================================================
// CREATE SPEECH RECOGNITION
// ==========================================================

else {

    recognition =
        new SpeechRecognition();


    recognition.lang =
        "en-IN";


    /*
        Keep this FALSE.

        We manually restart recognition after every command.
        This is generally more reliable for this setup.
    */

    recognition.continuous =
        false;


    recognition.interimResults =
        false;


    recognition.maxAlternatives =
        3;


    // ======================================================
    // ACTIVATE BUTTON
    // ======================================================

    button.addEventListener(
        "click",
        function () {


            // ------------------------------------------------
            // If JARVIS already active -> clicking button stops
            // ------------------------------------------------

            if (jarvisActivated) {

                stopJarvis();

                return;
            }


            // ------------------------------------------------
            // Activate JARVIS
            // ------------------------------------------------

            jarvisActivated = true;


            window.speechSynthesis.cancel();


            message.innerText =
                "VOICE SYSTEM INITIALIZED // Listening, Mohit...";


            startListening();
        }
    );


    // ======================================================
    // MICROPHONE START
    // ======================================================

    recognition.onstart =
        function () {


            recognitionActive = true;


            console.log(
                "VOICE CHANNEL OPEN"
            );


            setJarvisState(
                "LISTENING"
            );


            button.innerHTML =
                '<span class="mic-symbol">◉</span> JARVIS ACTIVE';
        };


    // ======================================================
    // USER SPEECH RESULT
    // ======================================================

    recognition.onresult =
        async function (event) {


            recognitionActive =
                false;


            // ------------------------------------------------
            // Get recognized command
            // ------------------------------------------------

            const command =
                event.results[0][0]
                    .transcript
                    .trim();


            console.log(
                "YOU:",
                command
            );


            if (!command) {

                startListening();

                return;
            }


            const commandLower =
                command.toLowerCase();


            // ==================================================
            // STOP VOICE COMMANDS
            // ==================================================

            if (

                commandLower.includes(
                    "jarvis stop listening"
                )

                ||

                commandLower.includes(
                    "stop jarvis"
                )

                ||

                commandLower.includes(
                    "jarvis go offline"
                )

                ||

                commandLower.includes(
                    "go offline jarvis"
                )

            ) {


                addTerminalLine(
                    "YOU",
                    command
                );


                jarvisActivated =
                    false;


                message.innerText =
                    "VOICE LINK TERMINATED";


                speak(
                    "Voice link closed. Goodbye Mohit."
                );


                return;
            }


            // ==================================================
            // PROCESS NORMAL COMMAND
            // ==================================================

            processingCommand =
                true;


            addTerminalLine(
                "YOU",
                command
            );


            setJarvisState(
                "THINKING"
            );


            message.innerText =
                "COMMAND RECEIVED // "
                + command;


            button.innerHTML =
                '<span class="mic-symbol">◉</span> PROCESSING COMMAND';


            try {


                // ==============================================
                // SEND COMMAND TO FLASK
                // ==============================================

                const response =
                    await fetch(
                        "/command",
                        {

                            method:
                                "POST",


                            headers: {

                                "Content-Type":
                                    "application/json"
                            },


                            body:
                                JSON.stringify({

                                    command:
                                        command
                                })
                        }
                    );


                // ==============================================
                // READ SERVER RESPONSE
                // ==============================================

                const data =
                    await response.json();


                console.log(
                    "SERVER RESPONSE:",
                    data
                );


                if (!data.reply) {

                    throw new Error(
                        "Server returned no reply."
                    );
                }


                // ==============================================
                // LOCAL COMMAND
                // ==============================================

                if (
                    data.type === "local"
                ) {


                    setJarvisState(
                        "EXECUTING"
                    );


                    message.innerText =
                        "EXECUTING // "
                        + data.reply;

                }


                // ==============================================
                // AI RESPONSE
                // ==============================================

                else {


                    message.innerText =
                        "JARVIS // "
                        + data.reply;
                }


                // ==============================================
                // TERMINAL
                // ==============================================

                addTerminalLine(
                    "JARVIS",
                    data.reply
                );


                // ==============================================
                // SPEAK RESPONSE
                // ==============================================

                speak(
                    data.reply
                );

            }


            // ==================================================
            // ERROR
            // ==================================================

            catch (error) {


                console.error(
                    "JARVIS ERROR:",
                    error
                );


                processingCommand =
                    false;


                setJarvisState(
                    "ERROR"
                );


                message.innerText =
                    "SYSTEM FAULT // Unable to process command.";


                // ----------------------------------------------
                // Start listening again after error
                // ----------------------------------------------

                if (jarvisActivated) {

                    setTimeout(
                        function () {

                            startListening();

                        },
                        1500
                    );
                }
            }
        };


    // ======================================================
    // MICROPHONE ERROR
    // ======================================================

    recognition.onerror =
        function (event) {


            recognitionActive =
                false;


            console.error(
                "VOICE ERROR:",
                event.error
            );


            // ==================================================
            // NO SPEECH
            // ==================================================

            if (
                event.error === "no-speech"
            ) {


                console.log(
                    "No speech detected."
                );


                if (jarvisActivated) {

                    message.innerText =
                        "VOICE CHANNEL OPEN // Awaiting command...";


                    setTimeout(
                        function () {

                            startListening();

                        },
                        600
                    );
                }


                return;
            }


            // ==================================================
            // ABORTED
            // ==================================================

            if (
                event.error === "aborted"
            ) {


                /*
                    Usually happens because we intentionally
                    stopped recognition before JARVIS speaks.
                */

                console.log(
                    "Recognition aborted."
                );


                return;
            }


            // ==================================================
            // OTHER ERRORS
            // ==================================================

            setJarvisState(
                "ERROR"
            );


            message.innerText =
                "VOICE MODULE ERROR // "
                + event.error;


            if (jarvisActivated) {

                setTimeout(
                    function () {

                        startListening();

                    },
                    1500
                );
            }
        };


    // ======================================================
    // MICROPHONE ENDED
    // ======================================================

    recognition.onend =
        function () {


            console.log(
                "VOICE CHANNEL CLOSED"
            );


            recognitionActive =
                false;


            /*
                Don't immediately restart if:

                - JARVIS is speaking
                - command is being processed
                - JARVIS has been deactivated
            */

            if (
                jarvisActivated
                &&
                !jarvisSpeaking
                &&
                !processingCommand
            ) {


                setTimeout(
                    function () {

                        startListening();

                    },
                    600
                );
            }
        };
}


// ==========================================================
// LOAD BROWSER VOICES
// ==========================================================

window.speechSynthesis.onvoiceschanged =
    function () {


        const voices =
            window.speechSynthesis
                .getVoices();


        console.log(
            "VOICE MODULES LOADED:",
            voices.length
        );
    };


// ==========================================================
// INITIAL STATE
// ==========================================================

setJarvisState(
    "READY"
);