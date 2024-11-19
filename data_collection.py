# Assumptions: all text files from Project Guntenberg begin with an introductory statement (Followed by * * *, after which the text of the book begins) and 
# are concluded with an ending statement (which is preceded by * * *, similarly). I remove these Project Gutenberg statements during cleaning. 
# However, I do not remove some details which would be found in a book such as table of contents; I assume this to be part of the text.
# I also assume that Project Gutenberg text files begin with a title, author, and language section. I use this to construct the metadata in my JSON.
# Only downloading the four Sherlock Holmes novels and the most popular collection of Sherlock Holmes short stories

import requests # Note -- external package
import re 
import json

# URLs for the 5 Sherlock Holmes books
URLS = [
    "https://www.gutenberg.org/cache/epub/244/pg244.txt",  # A Study in Scarlet
    "https://www.gutenberg.org/cache/epub/3289/pg3289.txt",  # The Valley of Fear
    "https://www.gutenberg.org/cache/epub/2097/pg2097.txt",  # The Sign of the Four
    "https://www.gutenberg.org/cache/epub/2852/pg2852.txt",  # The Hound of the Baskervilles
    "https://www.gutenberg.org/cache/epub/1661/pg1661.txt",  # The Adventures of Sherlock Holmes
    ]

# URL request; return plain text if successful 
def download_book(url):
    """Download a book's text from the given URL."""
    response = requests.get(url)
    if response.status_code == 200:  # HTTP status code for OK
        return response.text
    else:
        print(f"Failed to download book from {url}")
        return None

# Get title, author, and language from the downloaded text
def extract_metadata(raw_text):
    """Extract metadata from the raw text."""
    title_match = re.search(r"Title:\s*(.*?)\s*\n", raw_text)
    author_match = re.search(r"Author:\s*(.*?)\s*\n", raw_text)
    language_match = re.search(r"Language:\s*(.*?)\s*\n", raw_text)

    title = title_match.group(1) if title_match else "Unknown Title"
    author = author_match.group(1) if author_match else "Unknown Author"
    language = language_match.group(1) if language_match else "Unknown Language"

    return {"title": title, "author": author, "language": language}

# Load raw books, if available; if not, redownload them
def load_or_download_books():
    try: 
        with open("books_raw.json", "r", encoding="utf-8") as f:
            rawbooks = json.load(f) 
            if not rawbooks:  # Check if the file is empty
                raise ValueError("The JSON file is empty.")
    except (FileNotFoundError, ValueError):
        # Download books to a JSON file if they haven't been downloaded
        print("Error loading books_raw.json. Downloading books...")
        
        books = []
        for url in URLS:
            raw_text = download_book(url)
            if raw_text:
                metadata = extract_metadata(raw_text)
                metadata["text"] = raw_text  # Include the full raw text
                books.append(metadata)
        
        # Save all books to the JSON file
        with open("books_raw.json", "w", encoding="utf-8") as file:
            json.dump(books, file, indent=4)
            rawbooks = json.load(file)
    return rawbooks
