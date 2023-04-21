import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk


class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def search(self, word, max_edit_distance=2):
        current_row = range(len(word) + 1)
        corrections = []

        for char, child in self.root.children.items():
            self._recursive_search(child, char, word, current_row, corrections, max_edit_distance)

        return corrections

    def _recursive_search(self, node, word_so_far, word, prev_row, corrections, max_edit_distance):
        columns = len(word) + 1
        current_row = [prev_row[0] + 1]

        for column in range(1, columns):
            insert_cost = current_row[-1] + 1
            delete_cost = prev_row[column] + 1
            replace_cost = prev_row[column - 1] + (word_so_far[-1] != word[column - 1])
            current_row.append(min(insert_cost, delete_cost, replace_cost))

        if current_row[-1] <= max_edit_distance and node.is_end_of_word:
            corrections.append((current_row[-1], word_so_far))

        if min(current_row) <= max_edit_distance:
            for letter, child in node.children.items():
                self._recursive_search(child, word_so_far + letter, word, current_row, corrections, max_edit_distance)

def load_words_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        words = [line.strip() for line in file]
    return words

class AutocompleteApp(tk.Tk):
    def __init__(self, trie, image_path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Text Genie")
        self.trie = trie

        # Set window size
        self.geometry("1200x900")

        # Set font size
        style = ttk.Style()
        style.configure(".", font=("TkDefaultFont", 30))

        # Set color scheme
        self.configure(background="#269db5")
        style.configure(".", foreground="#2656b5", background="#2656b5")
        style.map(".", background=[("active", "#2656b5")])

        # Load and display image
        img = Image.open(image_path)
        img = img.resize((400, 400), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        self.img_label = ttk.Label(self, image=img)
        self.img_label.image = img
        self.img_label.pack(pady=20)

        self.word_entry = ttk.Entry(self, font=("TkDefaultFont", 30), foreground="#2656b5", background="#2656b5")
        self.word_entry.pack(padx=60, pady=60)
        self.word_entry.bind("<Return>", self.update_suggestions)

        self.suggestions_label = ttk.Label(self, text="", foreground="#26b586", background="#2656b5")
        self.suggestions_label.pack(padx=60, pady=60)

        self.word_entry.focus()

    def update_suggestions(self, event):
        input_word = self.word_entry.get()
        corrections = self.trie.search(input_word)

        if corrections:
            sorted_corrections = sorted(corrections, key=lambda x: (x[0], x[1]))
            suggested_words = [correction[1] for correction in sorted_corrections[:3]]
            self.suggestions_label.config(text="Suggestions: " + ", ".join(suggested_words))
        else:
            self.suggestions_label.config(text="No suggestions found.")

def main():
    trie = Trie()
    words = load_words_from_file("HCI-LLM-Project\HCI_LLM\dictionary.txt") 
    for word in words:
        trie.insert(word)

    # Replace 'path/to/your/image.png' with the path to the image you want to display
    image_path = 'HCI-LLM-Project\img.jpg'
    app = AutocompleteApp(trie, image_path)
    app.mainloop()

if __name__ == "__main__":
    main()