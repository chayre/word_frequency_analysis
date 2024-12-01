from os import path
import os
import numpy as np
from wordcloud import WordCloud # External
from PIL import Image
import matplotlib.pyplot as plt
import pandas as pd
# Graphing functions
def create_wordcloud(books_text, color_function):
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
        ax.set_title(title, fontsize=16, pad=10, loc='center')  # Add title above each subplot
    # Adjust layout and display
    plt.tight_layout()
    plt.show()

def create_barchart(books_common_words, color_map):
    # Plot most common words
    fig, axes = plt.subplots(nrows=1, ncols=len(books_common_words), figsize=(18, 6), sharey=True)
    # If there is only one subplot, axes will not be a list; convert to list
    if len(books_common_words) == 1:
        axes = [axes]
    for ax, (book, words) in zip(axes, books_common_words.items()):
        words, counts = zip(*words)
        # Assign colors based on the consistent color mapping
        colors = [color_map[word] for word in words]  
        bars = ax.bar(range(len(words)), counts, color=colors)  # Plot bars with the assigned colors
        ax.set_title(book, fontsize=12)
        ax.set_xticks(range(len(words)))  # Center ticks at bar positions
        ax.set_xticklabels(words, rotation=45, ha="center", fontsize=8)  
        ax.set_xlabel("Words", fontsize=12)
        ax.set_ylabel("Count", fontsize=12)
        ax.grid(axis="y", linestyle="--", alpha=0.7)
        # Annotate bars with count values
        for bar, count in zip(ax.patches, counts):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 5,
                    str(count), ha='center', va='bottom', fontsize=7)         
    # Main title and layout adjustments
    fig.suptitle("Top 10 Most Common Words for Each Book", fontsize=16)
    fig.tight_layout
    plt.show()
