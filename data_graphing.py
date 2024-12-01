from os import path
import os
import numpy as np
import pandas as pd
from wordcloud import WordCloud # External
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from random import seed
import re
from itertools import cycle
from data_analysis import calculate_mean_word_length

def generate_color_map(common_words):
    """
    Generate a color map dictionary based on the given common words.

    Args:
        common_words (dict): A dictionary with top N common words listed beside their count, for each text.
    """
    seed(3)
    return {word: cm.tab20(i % 20) for i, word in enumerate(sorted(common_words))}

def create_color_func(color_map):
    """
    Create a color function (and convert to RGB values) for the WordCloud library.
    
    Args:
        color_map (dict): A dictionary of words with predefined colors
    """
    def color_func(word, font_size, position, orientation, random_state=None, **kwargs):
        # Convert the color from float format to integer format (0-255)
        color = color_map.get(word, (0, 0, 0))  # Default to black if word is not in color_map
        return tuple(int(c * 255) for c in color[:3])  # Convert to RGB
    return color_func

def create_wordcloud(books_text, color_function):
    """
    Generate and plot a wordcloud for most common words.

    Args:
        books_text (dict): A dictionary of books with processed text.
        color_function (function): Passes colors assigned to most common words.
    """
    #Create mask in the shape of a magnifying glass
    d = path.dirname(__file__) if "__file__" in locals() else os.getcwd()
    mask_image = np.array(Image.open(path.join(d, "magnifier.png")))
    mask_image[mask_image == 0] = 255
    # Create subplots for word clouds
    fig, axes = plt.subplots(1, len(books_text), figsize=(20, 8))
    # If there is only one subplot, axes will not be a list; convert to list
    if len(books_text) == 1:
        axes = [axes]
    # Generate word clouds for each book and display
    for ax, (title, text) in zip(axes, books_text.items()):
        wc = WordCloud(
            background_color="white",
            mask=mask_image,
            width=1600,
            height=1000,
            color_func=color_function  # Apply consistent color function
        ).generate(text)
        ax.imshow(wc, interpolation="bilinear")
        ax.axis("off") 
        ax.set_title(title, fontsize=16, pad=10, loc='center') 
    # Adjust layout and display
    plt.tight_layout()
    plt.show()

def create_barchart(books_common_words, color_map, normalize=False, books_text=None):
    """
    Generate and plot barcharts for word counts or frequencies.

    Args:
        books_common_words (dict): A dictionary of books with their most common words and counts.
        color_map (dict): A mapping of words to colors for consistent visual representation.
        normalize (bool): Set to true to normalize word counts based on the total word count of the book. False by default.
        books_text (dict): A dictionary of books with their full text (needed for normalization).
    """
    # Calculate normalized frequencies if required
    if normalize and books_text:
        normalized_common_words = {}
        for title, words in books_common_words.items():
            total_words = len(books_text[title].split())
            normalized_common_words[title] = [(word, count / total_words) for word, count in words]
        books_common_words = normalized_common_words

    # Plot most common words
    fig, axes = plt.subplots(nrows=1, ncols=len(books_common_words), figsize=(18, 6), sharey=True)
    
    # If there is only one subplot, axes will not be a list; convert to list
    if len(books_common_words) == 1:
        axes = [axes] 
    for ax, (book, words) in zip(axes, books_common_words.items()):
        words, counts = zip(*words)  
        # Assign colors based on the consistent color mapping
        colors = [color_map[word] for word in words]
        bars = ax.bar(range(len(words)), counts, color=colors)   
        ax.set_title(book, fontsize=12)
        ax.set_xticks(range(len(words)))
        ax.set_xticklabels(words, rotation=45, ha="center", fontsize=7)
        ax.set_xlabel("Words", fontsize=12)
        ax.set_ylabel("Frequency" if normalize else "Count", fontsize=12)
        ax.grid(axis="y", linestyle="--", alpha=0.7)     
        # Annotate bars with count values
        if not normalize:
            for bar, count in zip(ax.patches, counts):
                ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.01, str(count), ha='center', va='bottom', fontsize=7
            )
    fig.suptitle(
        "Top 10 Most Common Words (Normalized by Total Words)" if normalize else "Top 10 Most Common Words",
        fontsize=16
    )
    fig.tight_layout()
    plt.show()

def create_mean_word_length_chart(text_dict, number_common_words):
    '''
    Create a line chart for the mean word lengths of the most common words in books.

    Args:
        text_dict (dict): A dictionary where keys are book titles and values are texts
        number_common_words (int): The number of most common words to calculate average length of 
    '''
    mean_lengths = calculate_mean_word_length(text_dict, number_common_words)
    # Convert to DataFrame
    df = pd.DataFrame(list(mean_lengths.items()), columns=['Book', 'Mean Word Length'])
    df['Index'] = np.arange(len(df))
    # Plot
    plt.figure(figsize=(10, 6))
    plt.plot(df['Index'], df['Mean Word Length'], marker='o', color='black', label='Mean Word Length')
    plt.xticks(df['Index'], df['Book'], rotation=30, ha='right', fontsize=10)
    plt.yticks(fontsize=10)
    for x, y in zip(df['Index'], df['Mean Word Length']):
        plt.text(x + 0.12, y - 0.02, f'{y:.2f}', ha='center', fontsize=10, color='blue')
    plt.title(f'Mean Word Length of the {number_common_words} Most Common Words in Sherlock Holmes Novels', fontsize=16)
    plt.xlabel('Books', fontsize=12)
    plt.ylabel('Mean Word Length', fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    # Display
    plt.tight_layout()
    plt.show()
