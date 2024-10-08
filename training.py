import json
import random
import webbrowser
import datetime
import speech_recognition as sr

# Load intents from JSON file
def load_intents(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Function to recognize speech
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio)
        print(f"You said: {command}")
        return command.lower()
    except sr.UnknownValueError:
        print("Sorry, I did not understand that.")
        return None
    except sr.RequestError:
        print("Could not request results; check your internet connection.")
        return None

# Function to process commands based on recognized speech
def process_command(command, intents):
    for intent in intents['intents']:
        for pattern in intent['patterns']:
            if pattern.lower() in command:
                if intent['tag'] == 'tell_time':
                    current_time = datetime.datetime.now().strftime('%H:%M:%S')
                    response = random.choice(intent['responses']).format(time=current_time)
                    return response
                elif intent['tag'] == 'open_website':
                    url = command.split("open website ")[-1]
                    webbrowser.open(url)
                    return f"Opening {url}."
                elif intent['tag'] == 'goodbye':
                    return random.choice(intent['responses'])
                else:
                    return random.choice(intent['responses'])

    return "I'm sorry, I didn't understand that."

def main():
    intents = load_intents('intents.json')  # Load intents from JSON file
    print("Assistant Bot is running! Say 'goodbye' to exit.")

    while True:
        command = recognize_speech()
        if command:
            response = process_command(command, intents)
            print("Bot:", response)
            if "goodbye" in command:
                break

if __name__ == "__main__":
    main()
