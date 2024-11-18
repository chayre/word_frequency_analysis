import re
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud # Note -- external package
import requests # Note -- external package
import json

# URL for Project Gutenberg book of interest (.txt)
def download_book(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Failed to download {url}")
        return ""

# Function to save the text to a file
def save_to_file(text, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(text)
    print(f"File saved to {file_path}")


def clean_text(text):
    # Remove the introductory Project Gutenberg text (before the actual book starts)
    text = re.sub(r"^.*?( \*\*\*)", "", text, flags=re.DOTALL)
    # Remove the end Project Gutenberg text (after the book ends)
    text = re.sub(r"(END OF THE PROJECT GUTENBERG EBOOK.*)", "", text, flags=re.DOTALL)

    # Remove digits
    text = re.sub(r"\d+", "", text)
     # Remove apostrophes
    text = text.replace("'", "")
    text = text.replace("’", "") # Accounts for funky ’, which differs from regular apostrophe '
    # Replace punctuation with space 
    text = re.sub(r"[^\w\s]", " ", text)  # This replaces all punctuation except letters and whitespace 
    # Replace dashes (hyphen, en dash, em dash) with spaces to preserve word separation
    text = re.sub(r"[\u2014\u2013-]", " ", text)  # This replaces em dash, en dash, and hyphen
    # Replace multiple spaces with a single space
    text = re.sub(r"\s+", " ", text)
    # Strip leading and trailing spaces
    text = text.strip()
    # Make all text lower-case
    text = text.lower()
    return text

# Clean the text by removing unwanted metadata and extracting necessary information
def extract_metadata(text):
    # Extract metadata information using regex
    title_match = re.search(r"Title:\s*(.*?)\s*\n", text)
    author_match = re.search(r"Author:\s*(.*?)\s*\n", text)
    language_match = re.search(r"Language:\s*(.*?)\s*\n", text)

    # Extracted metadata values
    title = title_match.group(1) if title_match else "Unknown Title"
    author = author_match.group(1) if author_match else "Unknown Author"
    language = language_match.group(1) if language_match else "Unknown Language"
    return title, author, language

#scarlet_book = download_book("https://www.gutenberg.org/cache/epub/244/pg244.txt") # A Study in Scarlet raw text
valley_book = download_book("https://www.gutenberg.org/cache/epub/3289/pg3289.txt") # The Valley of Fear raw text
#sign_book = download_book("https://www.gutenberg.org/cache/epub/2097/pg2097.txt") # The Sign of the Four raw text
#hound_book = download_book("https://www.gutenberg.org/cache/epub/2852/pg2852.txt") # The Hound of the Baskerviles raw text
#adventures_book = download_book("https://www.gutenberg.org/cache/epub/1661/pg1661.txt") # The Adventures of Sherlock Holmes raw text
#holmes_collection_raw = (scarlet_book, valley_book, sign_book, hound_book, adventures_book) # Tuple containing the raw downloaded text of all books

# Save file
#valley_text = clean_text(valley_book)
#save_to_file(valley_text, '/home/cayres/projects/word_frequency_analysis/the_valley_of_fear.txt')


#print(clean_text("don't you think!...** no-I can't"))
#print(clean_text(valley_book))
#print(extract_metadata(holmes_collection[0]))
#print(extract_metadata(holmes_collection[1]))
#print(extract_metadata(holmes_collection[2]))
#print(extract_metadata(holmes_collection[3]))
#print(extract_metadata(holmes_collection[4]))


# Save to JSON file
[
  {
    "title": "A Study in Scarlet",
    "author": "Arthur Conan Doyle",
    "language": "English",
    "year": 1887,
    "word_count": 67000,
    "text": "full text here"
  },
  {
    "title": "The Valley of Fear",
    "author": "Arthur Conan Doyle",
    "language": "English",
    "year": 1915,
    "word_count": 85000,
    "text": "full text here"
  },
  ...
]
