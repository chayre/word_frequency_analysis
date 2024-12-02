from collections import Counter
from itertools import chain
import re
import numpy as np
import pandas as pd

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