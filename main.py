""""Execute Code"""
#installed: sudo apt install libxcb-cursor0
from os import path
import json
from wordcloud import WordCloud # External
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import pandas as pd
from data_collection import load_or_download_books
from data_preprocessing import preprocess_all_books
import os 
from collections import Counter

#from data_processing 

def main():
    # Load raw books, if available; if not, redownload them
    # To test functionality, delete books_raw.json
    #books = load_or_download_books()

    # Preprocess each book (remove text, make lowercase, etc.) and update its text field
    #preprocess_all_books(books)

    # Save the processed text back to a new JSON file
    #with open("books_cleaned.json", "w", encoding="utf-8") as file:
        #json.dump(books, file, indent=4, ensure_ascii=False)  
        #print("All text has been preprocessed and saved to books_cleaned.json")

    # Read the processed text and analyze
    with open("books_cleaned.json", "r", encoding="utf-8") as f:
        cleaned_books = json.load(f)

    #first_book = ' '.join(cleaned_books[0]['text'])

    all_books_text = ''
    for i in range(0, len(cleaned_books)):
        all_books_text = all_books_text + (' '.join(cleaned_books[i]['text']))


    #Create mask in the shape of a magnifying glass
    d = path.dirname(__file__) if "__file__" in locals() else os.getcwd()
    mask_image = np.array(Image.open(path.join(d, "magnifier.png")))
    mask_image[mask_image == 0] = 255

    #Create and show Wordcloud
    wc = WordCloud(background_color = 'white', mask = mask_image, colormap = 'copper', width = 1600, height = 1000).generate(all_books_text)
    plt.axis("off")
    plt.imshow(wc)
    plt.show()

    # Count most common words
    def return_most_common(text, n):
        word_counts = Counter(text.split())
        most_common = word_counts.most_common(n)
        return most_common 
    
    overall_most_common = return_most_common(all_books_text, 20)

    # Example data: 10 most common words for each of 5 books
    books_common_words = {
        "A Study in Scarlet": return_most_common(' '.join(cleaned_books[0]['text']), 10),
        "Valley of Fear": return_most_common(' '.join(cleaned_books[1]['text']), 10),
        "Sign of the Four": return_most_common(' '.join(cleaned_books[2]['text']), 10),
        "Hound of the Baskervilles": return_most_common(' '.join(cleaned_books[3]['text']), 10),
        "Advntrs of Sherlock Holmes": return_most_common(' '.join(cleaned_books[4]['text']), 10),
    }

    #Combine data into a dataframe for easier processing
    all_words = set(word for book in books_common_words.values() for word, _ in book)
    data = {book: {word: count for word, count in words} for book, words in books_common_words.items()}
    df = pd.DataFrame(data).fillna(0)  # Fill missing words with 0

    #Focus on the top N words (e.g., 10 most common across all books)
    top_words = df.sum(axis=1).nlargest(10).index
    df = df.loc[top_words]

    #Plot the data
    df.T.plot(kind='bar', figsize=(12, 6), width=0.8)
    plt.title('Comparison of Most Common Words Across Books')
    plt.ylabel('Word Count')
    plt.xlabel('Books')
    plt.legend(title='Words', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()





if __name__ == "__main__":
    main()
