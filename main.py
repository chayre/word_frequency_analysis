""""Execute Code"""
#installed: sudo apt install libxcb-cursor0
import json
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
from data_collection import load_or_download_books
from data_preprocessing import preprocess_all_books

#from data_processing 

def main():
    # Load raw books, if available; if not, redownload them
    # To test functionality, delete books_raw.json
    books = load_or_download_books()

    # Preprocess each book (remove text, make lowercase, etc.) and update its text field
    preprocess_all_books(books)

    # Save the processed text back to a new JSON file
    with open("books_cleaned.json", "w", encoding="utf-8") as file:
        json.dump(books, file, indent=4, ensure_ascii=False)  
        print("All text has been preprocessed and saved to books_cleaned.json")

    # Read the processed text and analyze
    with open("books_cleaned.json", "r", encoding="utf-8") as f:
        cleaned_books = json.load(f)

    # Make a wordcloud

    first_book = ' '.join(cleaned_books[0]['text'])
    #wc = WordCloud().generate(first_book)


    magnifier = np.array(Image.open('./magnifier.png'))
    wc = WordCloud(background_color='white', mask = magnifier, colormap = 'binary',
        stopwords = ['meta'], width = 800, height = 500).generate(first_book)

    print(magnifier)
    magnifier
    #plt.imshow(wc)
    plt.imshow(wc, interpolation='bilinear')
    plt.axis("off")
    plt.show()



if __name__ == "__main__":
    main()
