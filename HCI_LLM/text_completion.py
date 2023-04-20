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

    def search(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]
        return self._collect_all_words(node, prefix)

    def _collect_all_words(self, node, prefix):
        words = []
        if node.is_end_of_word:
            words.append(prefix)
        for char, child in node.children.items():
            words += self._collect_all_words(child, prefix + char)
        return words
    

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
        prefix = input("Enter prefix: ")
        if prefix == "exit":
            break
        completions = trie.search(prefix)
        print("Completions:", completions)
        print(" ")                          #I added this to seperate outputs and make viewing easier 

if __name__ == "__main__":
    main()
