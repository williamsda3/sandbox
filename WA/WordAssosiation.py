import random
import requests
import json
import os


# Something I tend to do so that the terminal stays 'clean'
MAX_LINES = 10
output = []

def Print(text):
    
    global output

    # Add the new text to the output list
    output.append(text)

    # If the output list exceeds the max number of lines, remove the oldest line
    if len(output) > MAX_LINES:
        output.pop(0)

    # Clear the terminal
    os.system('cls')

    # Print the output list to the terminal
    print('\n'.join(output))
# Define your Merriam-Webster's API key here
API_KEY = "23a8b300-76e1-40cb-afd3-c258c8a30d10"

# Define a function to fetch related words from the API
def get_related_words(word):
    url = f"https://www.dictionaryapi.com/api/v3/references/thesaurus/json/{word}?key={API_KEY}"
    response = requests.get(url)
    data = json.loads(response.text)
    related_words = []
    for entry in data:
        if "meta" in entry and "syns" in entry["meta"]:
            for synset in entry["meta"]["syns"]:
                for syn in synset:
                    if syn != word:
                        related_words.append(syn)
    return related_words

# Define a list of starting words to use for the game
words = ["Coffee", "Java", "Type", "Scroll", "Math", "Computer", "Time", "Block", "Blue", "Beep", "Mouse"]

# Add some phrases that the game will say in response to the users choice
dialogues = ["Oo nice One! How about: ", "Interesting choice... that makes me think of: ", "When I hear that I think of: "]

# Some queries take a while to display, so I added some phrases that the game will say during that time
waitings = ["Hmmm...", "One sec...", "Thinking..."]

# Start the game
print("Welcome to Word Association! I'll say a word, and you respond with the first related word that comes to your mind. Let's begin!")
print( 'Current word: '+ random.choice(words))
current_word = input("What word comes to mind? ")

# Loop through the game until the user decides to quit
while True:
    
    # Get related words for the current word
    Print(random.choice(waitings))
    related_words = get_related_words(current_word)
    
    # Sometimes I would get an OoB error, seeing if this would fix it..
    if related_words:
        
       # Display games response
        Print(random.choice(dialogues)+ random.choice(related_words))
        response = input("Your turn: ")
        Print("Your turn: "+ response)
      
        # FIX; as of now the user needs to enter 'quit' for 2 turns to end the game
        if response.lower() == "quit":
            break
    else:
        print("I couldn't think of any related words for that. Let's try another word!")
        current_word = input("What word comes to mind? ")
       
        
       
       
# End the game
Print("Thanks for playing!")
