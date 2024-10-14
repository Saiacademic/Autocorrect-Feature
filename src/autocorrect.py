import re
from collections import Counter
from typos import correct_typos
from word_count import count_words
from constants import SUPPORTED_LANGUAGES
from pathlib import Path


class SpellCorrector:
    def __init__(self, language='english'):
        if language not in SUPPORTED_LANGUAGES:
            raise ValueError(f"Unsupported language: {language}")

        # Load the word frequency dictionary for the given language
        self.words = self.load_words(f'src/language_models/{language}.txt')
        self.word_counts = Counter(self.words)

    # Read and normalize the text file (word frequency file)
    def load_words(self, filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                return re.findall(r'\w+', file.read().lower())
        except FileNotFoundError:
            raise Exception(f"Dictionary file for {filepath} not found!")

    # Probability of a word based on its frequency
    def probability(self, word):
        N = sum(self.word_counts.values())
        return self.word_counts[word] / N if N else 0

    # Edit distance functions (edits are word variations)
    def edits1(self, word):
        letters = 'abcdefghijklmnopqrstuvwxyz'
        splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        deletes = [L + R[1:] for L, R in splits if R]
        transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
        replaces = [L + c + R[1:] for L, R in splits if R for c in letters]
        inserts = [L + c + R for L, R in splits for c in letters]
        return set(deletes + transposes + replaces + inserts)

    # Generate possible candidates for correction
    def candidates(self, word):
        return (self.known([word]) or
                self.known(self.edits1(word)) or
                [word])

    # Return the set of known words from the dictionary
    def known(self, words):
        return set(w for w in words if w in self.word_counts)

    # Correct a word by returning the best candidate
    def correct(self, word):
        return max(self.candidates(word), key=self.probability)


# Main function to use the spelling corrector
if __name__ == "__main__":
    corrector = SpellCorrector(language='english')
    text = input("Enter the text to correct: ").lower()

    corrected_text = ' '.join(corrector.correct(word) for word in text.split())
    print(f"Corrected text: {corrected_text}")

    # Show statistics from word count module
    word_count_stats = count_words(corrected_text)
    print(f"Word count stats: {word_count_stats}")

    # Optional: Handle common typos using the typo module
    typo_corrected_text = correct_typos(corrected_text)
    print(f"Typo-corrected text: {typo_corrected_text}")
