""""Execute Code"""
from data_collection import load_or_download_books
from data_preprocessing import process_all_books
import json

def main():
    # Load raw books, if available; if not, redownload them
    # To test functionality, delete books_raw.json
    rawbooks = load_or_download_books()

    # Process each book (remove text, make lowercase, etc.) and update its text field
    process_all_books(rawbooks)

    # Save the processed text back to a new JSON file
    with open("books_cleaned.json", "w", encoding="utf-8") as file:
        json.dump(rawbooks, file, indent=4, ensure_ascii=False)  # Save the updated JSON to a new file
        print("Books have been cleaned and saved to books_cleaned.json")

if __name__ == "__main__":
    main()
