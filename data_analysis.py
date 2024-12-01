#Analysis functions
from collections import Counter
import numpy as np

# Count most common words
def return_most_common(text, n):
    word_counts = Counter(text.split())
    most_common = word_counts.most_common(n)
    return most_common 

def calculate_mean_word_length(text_dict, number_common_words):
    '''
    Calculate the mean length of the most common words for each book.

    Args:
        common_words_dict (dict): A dictionary where keys are book titles and 
        values are lists of tuples (word, frequency), representing the most common words and their frequencies.
        number_common_words (int): The number of most common words to calculate average length of 
    '''
    common_words_dict = {title: return_most_common(text, number_common_words) for title, text in text_dict.items()}
    mean_lengths = {}
    for book, words in common_words_dict.items():
        # Extract the words and calculate their lengths
        word_lengths = np.array([len(word) for word, _ in words])
        # Compute the mean length
        mean_lengths[book] = round(float(np.mean(word_lengths)), 2)
    
    return mean_lengths
 
    # Display results
    for book, avg_length in word_lengths.items():
        print(f"Average word length in {book}: {avg_length:.2f}")