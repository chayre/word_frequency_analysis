from collections import Counter
from collections import defaultdict
from itertools import chain
from itertools import combinations
import itertools
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def unique_words_from_texts(book_texts):
    '''
    Identify unique words for each book based on their word frequencies.
    Return a dictionary with book titles as keys and unique words for each book as the value. 
    Args:
        book_texts (dict): Dictionary with book titles as keys and full text as values.
    '''
    #Tokenize and calculate word frequencies for the entire text (ignore spaces, punctuation)
    word_frequencies = {
        title: Counter(re.findall(r'\b\w+\b', text))  
        for title, text in book_texts.items()
    }
    word_sets = {title: set(freq.keys()) for title, freq in word_frequencies.items()}
    #Identify unique words for each book
    unique_words = {
        book: sorted(words - set(chain(*[word_sets[b] for b in word_sets if b != book])))
        for book, words in word_sets.items()
    }
    return unique_words

def return_most_common(text, number_common_words):
    '''
    Returns the top [number_common_words] most common words for a text.
    Args:
        text (string): The full text of the novel to be analyzed 
        number_common_words (int): What number of most common words to return 
    '''
    word_counts = Counter(text.split())
    most_common = word_counts.most_common(number_common_words)
    return most_common

def calculate_mean_word_length(text_dict, number_common_words):
    '''
    Calculate the mean length of the most common words for each book.
    Args:
        text (dict): A dictionary where keys are book titles and 
        values are full texts
        number_common_words (int): The number of most common words to calculate average length of 
    '''
    common_words_dict = {title: return_most_common(text, number_common_words) 
                        for title, text in text_dict.items()}
    mean_lengths = {}
    for book, words in common_words_dict.items():
        # Extract the words and calculate their lengths
        word_lengths = np.array([len(word) for word, _ in words])
        # Compute the mean length
        mean_lengths[book] = round(float(np.mean(word_lengths)), 2)
    return mean_lengths

def calculate_tf_idf(word_frequencies):
    '''
    Calculate TF-IDF scores for common words across books.
    Args:
        word_frequencies (dict): Dictionary with book titles as keys and list of tuples (word, frequency) as values.
    '''
    # Total number of documents
    num_texts = len(word_frequencies)
    # Convert frequencies to DataFrame
    data = []
    for book, freqs in word_frequencies.items():
        for word, freq in freqs:
            total_words = sum(f[1] for f in word_frequencies[book])
            data.append([book, word, freq, freq / total_words])
    tf_df = pd.DataFrame(data, columns=['Book', 'Word', 'Frequency', 'TF'])
    # Calculate IDF
    all_words = set(tf_df['Word'])
    idf_scores = {
        word: np.log(num_texts / sum(word in dict(freqs).keys() for freqs in word_frequencies.values()))
        for word in all_words
    }
    # Calculate TF-IDF
    tf_df['IDF'] = tf_df['Word'].map(idf_scores)
    tf_df['TF-IDF'] = tf_df['TF'] * tf_df['IDF']
    return tf_df

def calculate_word_pair_frequencies(all_text, common_word_list, window_size):
    """
    Calculate co-occurrence frequencies of common words within a window size in the given texts.

    Args:
        all_text (dict): Dictionary with title as key and corresponding full texts as value.
        common_word_list (dict): Dictionary with title as key and lists of common words as values.
        window_size (int): The size of the window to check for word co-occurrences.

    Returns:
        dict: Co-occurrence matrices for each text identifier.
    """
    cooccurrence_matrices = {}
    for book, text in all_text.items():
        # List of common words for the current book
        common_words = common_word_list[book]
        word_indices = [i for i, word in enumerate(text.split()) if word in common_words]

        # Initialize the co-occurrence matrix
        matrix = np.zeros((len(common_words), len(common_words)), dtype=int)
        word_to_index = {word: i for i, word in enumerate(common_words)}

        # Set to track already counted indices
        counted_indices = set()

        # Iterate through words and count co-occurrences
        words = text.split()
        idx = 0  # Pointer to the current word index
        while idx < len(word_indices):
            word_idx = word_indices[idx]
            if word_idx in counted_indices:
                idx += 1
                continue  # Skip if the word index has already been counted

            window_start = max(word_idx - window_size, 0)
            window_end = min(word_idx + window_size + 1, len(words))
            window_words_indices = [
                (i, words[i]) for i in range(window_start, window_end) if i not in counted_indices
            ]

            for i, (index1, word1) in enumerate(window_words_indices):
                for j, (index2, word2) in enumerate(window_words_indices[i + 1 :], start=i + 1):
                    if (
                        #word1 != word2
                        word1 in word_to_index
                        and word2 in word_to_index
                    ):
                        # Count the co-occurrence of the pair
                        matrix[word_to_index[word1], word_to_index[word2]] += 1
                        matrix[word_to_index[word2], word_to_index[word1]] += 1  # Symmetric
                        counted_indices.add(index1)
                        counted_indices.add(index2)
            # Increment the index to skip the word after counting
            counted_indices.add(word_idx)
            idx += 1

        cooccurrence_matrices[book] = matrix
    return cooccurrence_matrices

def generate_ngrams(text, n):
    """
    Generate a list of n-grams from a given text.
    Args:
        text (str): Input text.
        n (int): Size of n-grams to generate.
    """
    words = text.split()
    ngrams = list(itertools.islice(zip(*(words[i:] for i in range(n))), len(words) - n + 1))
    return ngrams

def analyze_ngrams(book_texts, n):
    """
    Analyze n-gram frequencies for a collection of books.
    Args:
        book_texts (dict): Dictionary with book titles as keys and full text as values.
        n (int): Size of n-grams to analyze.
    Returns:
        dict: Dictionary with book titles as keys and n-gram frequency counters as values.
    """
    ngram_frequencies = {
        title: Counter(generate_ngrams(text, n))
        for title, text in book_texts.items()
    }
    return ngram_frequencies