""""Execute Code"""
import json
from data_collection import load_or_download_books
from data_preprocessing import preprocess_all_books

def main():
    # Load raw books, if available; if not, redownload them
    # To test functionality, delete books_raw.json
    rawbooks = load_or_download_books()

    # Preprocess each book (remove text, make lowercase, etc.) and update its text field
    preprocess_all_books(rawbooks)

    # Save the processed text back to a new JSON file
    with open("books_cleaned.json", "w", encoding="utf-8") as file:
        json.dump(rawbooks, file, indent=4, ensure_ascii=False)  # Save the updated JSON to a new file
        print("All text has been preprocessed and saved to books_cleaned.json")

if __name__ == "__main__":
    main()
