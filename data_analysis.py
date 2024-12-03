from collections import Counter
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

def generate_word_pairs(words, window_size):
    '''
    Generate word pairs within a sliding window.

    Args:
    words (list): List of words (filtered to include only common words).
    window_size (int): The size of the sliding window for generating word pairs.

    Returns:
    list: A list of word pairs (tuples).
    '''
    word_pairs = []
    
    # Sliding window to generate word pairs
    for i in range(len(words) - window_size + 1):
        window = words[i:i + window_size]
        word_pairs.extend(combinations(window, 2))  # Generate all pairs within the window
    
    return word_pairs

def calculate_word_pair_frequencies(all_text, common_word_list, window_size):
    '''
    Calculate co-occurrence frequencies for word pairs within a sliding window.

    Args:
    all_text (dict): A dictionary where keys are book titles and values are full texts.
    common_word_list (dict): A dictionary where keys are book titles and values are lists of common words.
    window_size (int): The size of the sliding window for generating word pairs.

    Returns:
    pandas.DataFrame: Co-occurrence matrix (heatmap) of word pairs.
    '''
    # Initialize a Counter to track word pair frequencies
    pair_freq = Counter()

    for title, text in all_text.items():
        if title not in common_word_list:
            print(f"Skipping {title} as it has no common words defined.")
            continue

        # Get the list of common words for this book
        common_words = common_word_list[title]
        common_word_set = set(common_words)

        # Filter the text to only include common words
        filtered_words = [word for word in text.split() if word in common_word_set]
        
        # Generate word pairs using the sliding window
        word_pairs = generate_word_pairs(filtered_words, window_size)
        
        # Count the frequency of each pair
        for word1, word2 in word_pairs:
            pair_freq[(word1, word2)] += 1
            pair_freq[(word2, word1)] += 1  # Ensure the matrix is symmetric

    # Create a co-occurrence matrix
    unique_words = sorted(set([word for pair in pair_freq.keys() for word in pair]))
    word_index = {word: idx for idx, word in enumerate(unique_words)}
    
    # Initialize the co-occurrence matrix
    cooccurrence_matrix = np.zeros((len(unique_words), len(unique_words)), dtype=int)

    # Populate the co-occurrence matrix
    for (word1, word2), count in pair_freq.items():
        i, j = word_index[word1], word_index[word2]
        cooccurrence_matrix[i, j] = count
        cooccurrence_matrix[j, i] = count  # Symmetric matrix

    # Create a DataFrame for easier visualization
    cooccurrence_df = pd.DataFrame(cooccurrence_matrix, index=unique_words, columns=unique_words)

    return cooccurrence_df

def plot_cooccurrence_heatmap(cooccurrence_df):
    '''
    Plot a heatmap of the co-occurrence matrix.

    Args:
    cooccurrence_df (pandas.DataFrame): DataFrame containing the co-occurrence matrix.
    '''
    plt.figure(figsize=(10, 8))
    plt.title('Co-occurrence Heatmap')
    plt.imshow(cooccurrence_df, cmap='Blues', interpolation='none')
    plt.colorbar(label='Co-occurrence Count')
    plt.xticks(ticks=np.arange(len(cooccurrence_df.columns)), labels=cooccurrence_df.columns, rotation=90)
    plt.yticks(ticks=np.arange(len(cooccurrence_df.index)), labels=cooccurrence_df.index)
    plt.tight_layout()
    plt.show()