""""Execute Code"""
#installed: sudo apt install libxcb-cursor0
from os import path
import json
from matplotlib.cm import tab20
from matplotlib.colors import to_hex

from data_collection import load_or_download_books
from data_preprocessing import preprocess_all_books
from data_analysis import return_most_common
from data_graphing import create_wordcloud, create_barchart, create_mean_word_length_chart, generate_color_map, create_color_func



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

    # Text from each book in string format to generate WordCloud
    books_text = {book['title']: ' '.join(book['text']) for book in cleaned_books}

    # Text from all novels in string format
    all_text = {
        "Sherlock Holmes Novels": ' '.join(books_text.values()),
    }

    # 10 most common words for each book
    books_common_words = {title: return_most_common(text, 10) for title, text in books_text.items()}

    # 10 most common words for all of the novels
    all_text_common_words  = {
        "Sherlock Holmes Novels": return_most_common(all_text["Sherlock Holmes Novels"], 10),
    }

    # Take the most common words and assign a color to them which is consistent for graphical analysis
    # WordClouds use a color function; Barcharts use a color mapping
    common_words = set(word for book in books_common_words.values() for word, _ in book)
    color_map = generate_color_map(common_words)
    color_func = create_color_func(color_map)

   
    # Create 5 wordclouds for each of the novels
    create_wordcloud(books_text, color_func)

    # Create a wordcloud which shows the most common words for all novels
    create_wordcloud(all_text, color_func)

    # Create 5 barcharts to compare counts of most common words
    create_barchart(books_common_words, color_map)

    # Create 5 barcharts to compare frequency of most common words
    create_barchart(books_common_words, color_map, True, books_text)

    # Create a barchart which shows the most common words for all novels
    create_barchart(all_text_common_words, color_map)

    # Create a line chart which shows the average length of the top n (in this case, 50) words for each novel
    create_mean_word_length_chart(books_text, 30)

if __name__ == "__main__":
    main()
