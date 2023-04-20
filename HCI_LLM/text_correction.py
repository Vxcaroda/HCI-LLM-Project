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

def main():
    trie = Trie()
    words = load_words_from_file("HCI-LLM-Project\HCI_LLM\dictionary.txt")
    for word in words:
        trie.insert(word)

    while True:
        input_word = input("Enter a word: ")
        if input_word == "exit":
            break
        corrections = trie.search(input_word)
        if corrections:
            sorted_corrections = sorted(corrections, key=lambda x: (x[0], x[1]))
            print("Corrections:", [correction[1] for correction in sorted_corrections])
        else:
            print("No corrections found.")

if __name__ == "__main__":
    main()
