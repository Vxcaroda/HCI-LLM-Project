import re
import tkinter as tk
import tkinter.ttk as ttk
from collections import defaultdict, Counter
from PIL import Image, ImageTk

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


class PredictionApp(tk.Tk):
    def __init__(self, bigrams, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Sentence Sage")
        self.bigrams = bigrams

        # Set window size
        self.geometry("1200x800")

        # Set font size
        style = ttk.Style()
        style.configure(".", font=("TkDefaultFont", 20))

        # Set color scheme
        self.configure(background="#ffdee5")
        # style.configure(".", foreground="#2656b5", background="#2656b5")
        style.map(".", background=[("active", "#2656b5")])

        # Load and display image
        img = Image.open('HCI-LLM-Project\HCI_LLM\landscape.webp')
        img = img.resize((600, 600), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        self.img_label = ttk.Label(self, image=img)
        self.img_label.image = img
        self.img_label.pack(pady=20)

        self.sentence_entry = ttk.Entry(self, font=("TkDefaultFont", 20), width=150)
        self.sentence_entry.pack(padx=60, pady=60)
        self.sentence_entry.bind("<Return>", self.predict_and_show_next_word)

        self.sentence_entry.focus()

    def predict_and_show_next_word(self, event):
        input_sentence = self.sentence_entry.get()
        input_words = tokenize(input_sentence)
        last_word = input_words[-1]

        next_word = predict_next_word(self.bigrams, last_word)
        if next_word:
            self.sentence_entry.insert(tk.END, " " + next_word)
        else:
            self.sentence_entry.insert(tk.END, " (Unable to predict next word)")

def main():
    filename = "HCI-LLM-Project\HCI_LLM/text8.txt"
    training_text = read_training_text(filename)

    words = tokenize(training_text)
    bigrams = train_bigrams(words)

    app = PredictionApp(bigrams)
    app.mainloop()

if __name__ == "__main__":
    main()