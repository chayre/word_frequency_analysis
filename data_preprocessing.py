
import re
import requests # Note -- external package
import json


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