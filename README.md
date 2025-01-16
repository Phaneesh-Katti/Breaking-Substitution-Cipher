# Breaking-Substitution-Cipher

A powerful Python tool for breaking substitution ciphers using statistical analysis and smart optimization techniques. 

## Table of Contents
- [What is a Substitution Cipher?](#what-is-a-substitution-cipher)
- [Repository Contents](#repository-contents)
- [How This Decoder Works](#how-this-decoder-works)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Advanced Features](#advanced-features)
- [How It Works In Detail](#how-it-works-in-detail)
- [Contributing](#contributing)

## What is a Substitution Cipher?

A substitution cipher is one of the simplest forms of encryption where each letter in the plaintext is replaced with another letter or symbol. For example:

```
Plain alphabet:    ABCDEFGHIJKLMNOPQRSTUVWXYZ
Substituted with:  QWERTYUIOPASDFGHJKLZXCVBNM
```

So, the message "HELLO" might become "ITSSG" using this substitution key. While simple, there are 26! (approximately 4 × 10²⁶) possible keys, making brute force impractical.

## Repository Contents

This repository contains the following key files:

1. `main.py` - The main program file with the user interface
2. `decipher_text.py` - The core decryption engine
3. `quadgrams.txt` - Statistical data file for English quadgrams
4. `config.json` - Configuration file containing settings

## How This Decoder Works

This decoder uses several sophisticated techniques to break substitution ciphers:

1. **Statistical Analysis**: Uses quadgram (4-letter combinations) statistics from English text to score potential solutions
2. **Hill Climbing Algorithm**: Optimizes the solution by making small changes and keeping improvements
3. **Multiple Starting Points**: Tries different random starting positions to avoid local maxima
4. **Anchor Characters**: Preserves special characters (like spaces, punctuation) to maintain text structure
5. **English Word Recognition**: Validates solutions against common English words

## Features

- Fast and efficient decryption using hill-climbing algorithm
- User-friendly interface with two input methods:
  - Direct text input
  - File upload via browse dialog
- Handles special characters and preserves text formatting
- Configurable anchor characters (punctuation, spaces, etc.)
- Customizable common word list for validation
- Multiple solution variants with scoring
- Time-limited execution with graceful interruption
- Detailed progress reporting

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/substitution-cipher-decoder
cd substitution-cipher-decoder
```

2. Ensure all required files are present:
   - `main.py`
   - `decipher_text.py`
   - `quadgrams.txt`
   - `config.json`

3. Required Python packages:
   - `tkinter` (usually comes with Python)

## Usage

Run the program using:
```bash
python main.py
```

The program will present two options:
1. Enter ciphertext manually
2. Browse for a .txt file containing the ciphertext

For best results:
- Use longer texts (ideally 200+ characters)
- Include spaces and punctuation in the ciphertext
- Ensure the text is properly formatted

## Configuration

The `config.json` file contains two main sections:

```json
{
    "cipher_settings": {
        "anchor_chars": [" ", ".", ",", "!", "?", "-", ";", ":"],
        "common_words": ["the", "be", "to", "of", "and", ...]
    }
}
```

### Anchor Characters

Anchor characters are special characters that remain unchanged during decryption. They're crucial because:
- They preserve text structure and readability
- They provide word boundaries that help in validation
- They improve the accuracy of the statistical analysis

Default anchor characters include spaces, punctuation marks, and special symbols. You can modify these based on your needs.

### Common Words List

The common words list is used to validate potential solutions by checking what percentage of decrypted words appear in English. The default list includes:
- Most frequent English words
- Common pronouns, articles, and prepositions
- Basic verb forms

Tips for customizing the common words list:
1. Add domain-specific vocabulary if working with specialized texts
2. Include more verb forms and tenses for better recognition
3. Consider adding common contractions and their expanded forms
4. Keep the list focused on truly common words to avoid false positives

## How It Works In Detail

### 1. Text Preprocessing
- Converts input to uppercase for consistency
- Identifies and preserves anchor characters
- Maps special characters to unused English letters for processing

### 2. Statistical Analysis
- Uses quadgram statistics from English text
- Calculates log probabilities for better numerical stability
- Scores potential solutions based on frequency patterns
- This means that, larger the cipher text to decode, the better, as they will better follow the statistical analysis of the English language

### 3. Hill Climbing Algorithm
The decoder uses a hill-climbing algorithm that:
1. Starts with a random key
2. Makes small changes (swapping two letters)
3. Evaluates the new solution using:
   - Quadgram statistics score
   - Percentage of recognized English words
4. Keeps changes that improve the solution
5. Repeats until no improvement is found or time limit is reached

### 4. Solution Validation
Multiple validation techniques ensure good results:
- Statistical scoring using quadgrams
- English word percentage calculation
- Multiple random restarts to avoid local maxima
- Time-limited execution with best results storage

## Performance Considerations

The decoder's performance depends on:
- Length of input text (longer texts generally give better results)
- Quality of the common words list
- Number of iterations allowed
- Time limit set for processing

Tips for better results:
1. Use longer input texts (200+ characters recommended)
2. Include spaces and punctuation in the ciphertext
3. Increase the common words list for your specific domain
4. Adjust the time limit based on text length

## Contributing

Contributions are welcome! Here are some areas where you can help:
- Expanding the common words list
- Improving the statistical analysis
- Adding support for other languages
- Optimizing the hill-climbing algorithm
- Adding more validation techniques

Please submit pull requests or open issues for any improvements you'd like to suggest.
