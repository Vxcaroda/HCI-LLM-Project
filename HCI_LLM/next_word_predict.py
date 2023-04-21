import re
from collections import defaultdict, Counter

def read_training_text(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read()

def tokenize(text):
    words = re.findall(r'\b\w+\b', text.lower())
    return words

def train_bigrams(words):
    bigrams = defaultdict(Counter)
    for i in range(len(words) - 1):
        bigrams[words[i]][words[i + 1]] += 1
    return bigrams

def predict_next_word(bigrams, current_word):
    if not bigrams[current_word]:
        return None
    most_common_word = bigrams[current_word].most_common(1)[0][0]
    return most_common_word

def main():
    filename = "HCI-LLM-Project\HCI_LLM/text8.txt" 
    training_text = read_training_text(filename)

    words = tokenize(training_text)
    bigrams = train_bigrams(words)

    while True:
        input_sentence = input("Enter a sentence (type 'exit' to quit): ")
        if input_sentence.lower() == 'exit':
            break
        input_words = tokenize(input_sentence)
        last_word = input_words[-1]

        next_word = predict_next_word(bigrams, last_word)
        if next_word:
            print("Predicted next word:", next_word)
        else:
            print("Sorry, unable to predict the next word.")

if __name__ == "__main__":
    main()
