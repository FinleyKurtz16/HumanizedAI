# Bibliothek/en für die Eingabe (STT, ...)
import speech_recognition as sr
import time

# Bibliothek/en für das Vergleichen von Antworten (ob etwas [nicht] zutrifft)
from difflib import SequenceMatcher

# Bibliothek/en für das Abrufen/Speichern/Laden von Datenbanken
import os
import json

# Bibliothek/en für das Verarbeiten der Frage
from freeGPT import AsyncClient
import asyncio

# Bibliothek/en für das Ausgeben der Antwort (Output)
import gtts
from playsound import playsound

# Importiere die Completion-Klasse aus der completion.py Datei
from completition import Completion

# Initialisieren des Recognizer-Objekts
r = sr.Recognizer()

# Funktion zur Berechnung der Ähnlichkeit zwischen zwei Zeichenketten
def aehnlichkeit(a, b):
    return SequenceMatcher(None, a, b).ratio()

# Pfade zu den Datenbankdateien
QUESTIONS_PATH = "fragen_datenbank.txt"
ANSWERS_PATH = "antworten_datenbank.txt"

# Funktion zum Abrufen der Antwort aus der Datenbank
def get_answer_from_database(question):
    if os.path.exists(QUESTIONS_PATH) and os.path.exists(ANSWERS_PATH):
        with open(QUESTIONS_PATH, "r") as q_file, open(ANSWERS_PATH, "r") as a_file:
            questions = q_file.readlines()
            answers = a_file.readlines()
            for i, q in enumerate(questions):
                if aehnlichkeit(question, q.strip()) > 0.6:
                    return answers[i].strip()
    return None

# Funktion zum Speichern der Frage und Antwort in den Datenbanken
def save_question_and_answer_to_database(question, answer):
    with open(QUESTIONS_PATH, "a", encoding="utf-8") as q_file, open(ANSWERS_PATH, "a", encoding="utf-8") as a_file:
        q_file.write(question + "\n")
        a_file.write(answer + "\n")

# Funktion zur Umwandlung von Sprache in Text
class SpeechToText:
    def __init__(self, timeout=30, phrase_time_limit=20):
        self.recognizer = sr.Recognizer()
        self.timeout = timeout
        self.phrase_time_limit = phrase_time_limit

    def listen(self):
        with sr.Microphone() as source:
            print("Bitte sprechen Sie jetzt...")
            audio = self.recognizer.listen(source, timeout=self.timeout, phrase_time_limit=self.phrase_time_limit)
            print("Aufnahme beendet.")
        return audio

    def recognize(self, audio):
        try:
            text = self.recognizer.recognize_google(audio, language='de-DE')
            print("Ihr Text: " + text)
            return text
        except sr.UnknownValueError:
            print("Google Speech Recognition konnte die Audio nicht verstehen")
        except sr.RequestError as e:
            print("Fehler bei der Anforderung von Google Speech Recognition service; {0}".format(e))

class ProcessInput:
    def __init__(self, text):
        self.text = text
        self.completion = Completion()

    def is_already_answer(self):
        return get_answer_from_database(self.text)

    def is_already_command(self):
        from Commands import handle_commands
        return handle_commands(self.text)

    async def falcon_40b(self):
        try:
            resp = await AsyncClient.create_completion("gpt3", self.text)
            return resp
        except Exception as e:
            return ("Error: " + str(e))

    def gpt3_completion(self):
        try:
            return self.completion.create(self.text)
        except Exception as e:
            return ("Error: " + str(e))

    def save_question_and_answer(self, answer):
        save_question_and_answer_to_database(self.text, answer)

    def apply_personality(self, answer):
        # Hier müssen Sie den Code hinzufügen, um die Persönlichkeit zu überprüfen und anzupassen
        return answer

    def search_emotion(self, answer):
        # Hier müssen Sie den Code hinzufügen, um die Emotionen zu erkennen
        return answer

    def apply_emotion(self, answer):
        # Hier müssen Sie den Code hinzufügen, um die Emotionen anzuwenden
        return answer

    async def process(self):
        answer = self.is_already_command()
        if answer is None:
            answer = self.is_already_answer()
            if answer is None:
                answer = self.gpt3_completion()
                self.save_question_and_answer(answer)
        answer = self.apply_personality(answer)
        answer = self.search_emotion(answer)
        answer = self.apply_emotion(answer)
        return answer

# Funktion zur Umwandlung von Text in Sprache
def text_to_speech(answer):
    tts = gtts.gTTS(answer, lang='de')
    tts.save("answer.mp3")
    playsound("answer.mp3")

# Erstellen einer Instanz der SpeechToText Klasse
stt = SpeechToText()

# Aufnehmen von Audio und Umwandlung in Text
audio = stt.listen()
text = stt.recognize(audio)

# Verarbeiten der Eingabe und Ausgeben der Antwort
processor = ProcessInput(text)
answer = asyncio.run(processor.process())
print(answer)

# Text-To-Speech funktioniert noch nicht
## Umwandlung von Text in Sprache
## text_to_speech(answer)
