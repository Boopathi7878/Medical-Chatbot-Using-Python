import random
import json
import pickle
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer

# Initialize the lemmatizer and load necessary files
lemmatizer = WordNetLemmatizer()

# Load the intents file with correct path
intents = json.loads(open(r'C:\path\to\intents.json').read())  
words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))

# Placeholder function for simple predictions
def predict_class(sentence):
    """Predicts the class (intent) for the given sentence using a simple heuristic."""
    # Create a bag of words representation
    bag = bag_of_words(sentence)
    # Simple threshold for prediction
    # For demonstration, we'll just return a random class
    # Replace this logic with actual model inference logic
    max_index = np.argmax(bag)
    return [{'intent': classes[max_index], 'probability': str(bag[max_index])}]

def clean_up_sentence(sentence):
    """Tokenizes and lemmatizes the input sentence."""
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

def bag_of_words(sentence):
    """Creates a bag of words array for the input sentence."""
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        if w in words:
            bag[words.index(w)] = 1
    return np.array(bag)

def get_response(intents_list, intents_json):
    """Fetches a random response for the predicted intent."""
    if not intents_list:
        return "Sorry, I didn't understand that."
    
    tag = intents_list[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            return random.choice(i['responses'])
    
    return "Sorry, I didn't find a suitable response."

print("GO! Bot is running!")

# Infinite loop for chatbot interaction
while True:
    try:
        message = input("You: ")
        ints = predict_class(message)
        res = get_response(ints, intents)
        print("Bot:", res)
    except KeyboardInterrupt:
        print("\nExiting... Have a great day!")
        break
