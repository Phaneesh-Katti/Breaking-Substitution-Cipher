
import random
import re
import json
from math import log10
import time
import signal

class ngram_score(object):
    def __init__(self, ngram_file, sep=' '):
        """Load ngrams from a file, calculate log probabilities."""
        self.ngrams = {}
        with open(ngram_file, 'r') as f:
            for line in f:
                key, count = line.strip().split(sep)
                self.ngrams[key] = int(count)
        self.L = len(key)
        self.N = sum(self.ngrams.values())
        # Calculate log probabilities
        for key in self.ngrams.keys():
            self.ngrams[key] = log10(float(self.ngrams[key]) / self.N)
        self.floor = log10(0.01 / self.N)

    def score(self, text):
        """Compute the ngram score of the text."""
        score = 0
        ngrams = self.ngrams.__getitem__
        for i in range(len(text) - self.L + 1):
            if text[i:i + self.L] in self.ngrams:
                score += ngrams(text[i:i + self.L])
            else:
                score += self.floor
        return score


class DecipherText(object):
    def __init__(self, config):
        self.best_deciphers = []  # To store best deciphered text variations
        self.special_to_english = {}
        self.reversed_mapping = {}
        
        # Read settings from config
        self.anchor_chars = config["cipher_settings"]["anchor_chars"]
        self.common_words = config["cipher_settings"]["common_words"]

    def decipher(self, ciphertext):  
        """Decipher the given ciphertext"""

        # Load quadgram statistics
        fitness = ngram_score("quadgrams.txt")

        def check_english_percentage(text):
            """
            Calculate percentage of words in the text that look like English words.
            (Uses a basic heuristic of checking common word patterns instead of nltk.)
            """
            words_in_text = re.findall(r'\b[A-Za-z]+\b', text.lower())  # Split text into words
            if not words_in_text:
                return 0

            english_word_count = sum(1 for word in words_in_text if word in self.common_words)
            percentage = (english_word_count / len(words_in_text)) * 100
            return percentage

        def substitute_decrypt(text, key):
            """Decrypts text using a substitution cipher with the provided key."""
            key_map = {chr(i + 65): key[i] for i in range(26)}  # Map A-Z to substitution key
            reverse_map = {v: k for k, v in key_map.items()}    # Reverse key map for decryption
            return ''.join(reverse_map.get(char, char) for char in text)

        def dynamic_transform(ciphertext, anchor_chars):
            """
            Dynamically transform the ciphertext:
            - Identify English alphabets used and unused in the ciphertext.
            - Replace non-anchor special characters with unused English alphabets.
            """
            # Convert anchor_chars to a set for easier subtraction
            anchor_chars_set = set(anchor_chars)
            
            # Used characters are the characters in the ciphertext that are not anchor characters
            used_chars = set(ciphertext) - anchor_chars_set
            
            used_english = {char for char in used_chars if 'A' <= char <= 'Z'}
            special_chars = used_chars - used_english

            unused_english = [chr(i) for i in range(65, 91) if chr(i) not in used_english]

            special_to_english = {}
            for special, unused in zip(special_chars, unused_english):
                special_to_english[special] = unused

            transformed_text = ''.join(
                special_to_english.get(char, char) for char in ciphertext
            )

            return transformed_text, special_to_english

        def restore_anchors(transformed_text, anchor_positions):
            """
            Restores anchor characters to their original positions in the text.
            """
            result = list(transformed_text)
            for pos, char in sorted(anchor_positions):
                result.insert(pos, char)
            return ''.join(result)

        # Record anchor positions
        anchor_positions = [(i, char) for i, char in enumerate(ciphertext) if char in self.anchor_chars]

        # Transform ciphertext dynamically
        ctext, special_to_english = dynamic_transform(ciphertext.upper(), self.anchor_chars)
        self.special_to_english = special_to_english  # Store this mapping for later reversal

        # Reverse the mapping of special characters to unused English letters (for the key)
        self.reversed_mapping = {v: k for k, v in special_to_english.items()}

        # Remove non-English and non-anchor characters for decryption
        ctext = re.sub('[^A-Z]', '', ctext)

        MAX_ITERATIONS = 1000
        initial_key = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

        start_time = time.time()
        TIME_LIMIT = 300  # Maximum time in seconds

        def signal_handler(sig, frame):
            """Handle Ctrl+C gracefully."""
            print("\nProcess interrupted. Exiting...")
            self.print_top_results()  # Print top results before exiting
            self.print_reversed_key(current_key)  # Ensure the reversed key is printed when interrupted
            exit(0)

        signal.signal(signal.SIGINT, signal_handler)

        for iteration in range(MAX_ITERATIONS):
            if time.time() - start_time > TIME_LIMIT:
                print("\nTime limit reached. Exiting...")
                self.print_top_results()  # Print top results before exiting
                self.print_reversed_key(current_key)  # Ensure the reversed key is printed at timeout
                break

            random.shuffle(initial_key)
            current_key = initial_key[:]
            current_score = fitness.score(substitute_decrypt(ctext, current_key))

            for _ in range(1000):
                a, b = random.sample(range(26), 2)
                new_key = current_key[:]
                new_key[a], new_key[b] = new_key[b], new_key[a]

                deciphered_text = substitute_decrypt(ctext, new_key)
                new_score = fitness.score(deciphered_text)

                if new_score > current_score:
                    current_key = new_key
                    current_score = new_score

            deciphered_text = substitute_decrypt(ctext, current_key)
            restored_plaintext = restore_anchors(deciphered_text, anchor_positions)
            english_percentage = check_english_percentage(restored_plaintext)

            # Store best deciphered text variations
            reversed_key = self.get_reversed_key(current_key)
            self.best_deciphers.append((restored_plaintext, english_percentage, current_key, reversed_key))
            self.best_deciphers = sorted(self.best_deciphers, key=lambda x: x[1], reverse=True)[:3]

            print(f"Iteration {iteration + 1}:")
            print(f"Deciphered Plaintext: {restored_plaintext}")
            print(f"Score: {current_score}")
            print(f"English Percentage: {english_percentage:.2f}%")
            print(f"Key: {''.join(current_key)}")
            self.print_reversed_key(current_key)
            print("=" * 50)

        # Final print of top 3 results after interruption or timeout
        self.print_top_results()

    def get_reversed_key(self, current_key):
        """Generate and return the reversed key based on the original cipher text characters."""
        return [self.reversed_mapping.get(char, char) for char in current_key]

    def print_reversed_key(self, current_key):
        """Reverses the mapping of the transformed key and prints the key in terms of the original cipher text characters."""
        key_in_original_text = []
        for char in current_key:
            if char.isalpha():  # If it's a letter
                # Get the corresponding original cipher text character
                original_char = self.reversed_mapping.get(char, char)
                key_in_original_text.append(original_char)
            else:
                key_in_original_text.append(char)  # Non-alphabet characters remain as is

    def print_top_results(self):
        """Print the top 3 deciphered text variations based on English percentage."""
        print("\nTop 3 Deciphered Text Variations:")
        for idx, (deciphered_text, percentage, current_key, reversed_key) in enumerate(self.best_deciphers, 1):
            print(f"Rank {idx}:")
            print(f"Deciphered Text: {deciphered_text}")
            print(f"English Percentage: {percentage:.2f}%")
            print(f"Key: {''.join(reversed_key)}")
            print("=" * 50)

