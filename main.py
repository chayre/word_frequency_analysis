"""Execute code from other scripts in main()"""
import json
from data_collection import load_or_download_books
from data_preprocessing import preprocess_all_books
from data_analysis import return_most_common, unique_words_from_texts, calculate_tf_idf, calculate_word_pair_frequencies, analyze_ngrams, update_missing_words
from data_graphing import create_wordcloud, create_barchart, create_mean_word_length_chart, generate_color_map, create_color_func, plot_tfidf_heatmap, plot_cooccurrence_heatmap, plot_ngrams

def main():
    # Load raw books, if available; if not, redownload them
    # To test functionality, delete books_raw.json
    books = load_or_download_books()

    # Preprocess each book (remove text, make lowercase, etc.) and update its text field
    preprocess_all_books(books)

    # Save the processed text back to a new JSON file
    with open("books_cleaned.json", "w", encoding="utf-8") as file:
        json.dump(books, file, indent=4, ensure_ascii=False)

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

    # 50 most common words for all of the novels (without count)
    common_word_list = {
        book: [word for word, _ in words]
        for book, words in {
        "Sherlock Holmes Novels": return_most_common(all_text["Sherlock Holmes Novels"], 50),
        }
        .items()
    }

    # Take the most common words and assign a color to them which is consistent for graphical analysis. Wordclouds use a color function, barcharts use a color mapping
    common_words = set(word for book in books_common_words.values() for word, _ in book)
    color_map = generate_color_map(common_words)
    color_func = create_color_func(color_map)

    # Create 5 wordclouds for each of the novels showing most common words
    create_wordcloud(books_text, color_func)

    # Create a wordcloud which shows the most common words for all novels
    create_wordcloud(all_text, color_func)

    # Create 5 barcharts to compare counts of most common words
    create_barchart(books_common_words, color_map)

    # Create 5 barcharts to compare frequencies of most common words
    create_barchart(all_text_common_words, color_map)

    # Create a line chart which shows the average length of the top n (in this case, 50) words for each novel
    create_mean_word_length_chart(books_text, 50)

    # Create 5 wordclouds for each of the novels, showing unique words in each
    create_wordcloud({title: ' '.join(words) for title, words in unique_words_from_texts(books_text).items()}, color_func, True)

    #Plot standard tfidf heatmap
    plot_tfidf_heatmap(calculate_tf_idf(update_missing_words(books_common_words, books_text), books_text))

    #Plot smooth tfidf heatmap
    plot_tfidf_heatmap(calculate_tf_idf(update_missing_words(books_common_words, books_text), books_text, smooth=True), smooth=True)

    # Create a co-occurrence heatmap for the 50 most common words (windowsize 1, which looks at the words next to each common word - 3 word segments)
    plot_cooccurrence_heatmap(calculate_word_pair_frequencies(all_text, common_word_list, 1), common_word_list, 1)

    # Plot the top 10 2-word combinations for each book in the collection (itertools)
    plot_ngrams(analyze_ngrams(books_text, 2), 10, 2)

    # Plot the top 10 2-word combinations for all Sherlock Holmes Novels
    plot_ngrams(analyze_ngrams(all_text, 2), 10, 2)

if __name__ == "__main__":
    main()
