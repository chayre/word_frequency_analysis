"""Process the raw data so that it is ready for textual analysis"""
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('omw-1.4', quiet=True)

def preprocess_text(text):
    """Convert raw text to preprocessed text."""
    # Make all text lower-case
    text = text.lower()
    # Remove the introductory Project Gutenberg text (before the book starts)
    text = re.sub(r"^.*?( \*\*\*)", "", text, flags=re.DOTALL)
    # Remove the end Project Gutenberg text (after the book ends)
    text = re.sub(r"(end of the project gutenberg.*)", "", text, flags=re.DOTALL)
    # Remove digits
    text = re.sub(r"\d+", "", text)
    # Remove Roman numerals (chapter numbers)
    text = re.sub(r"\b(ii|iii|iv|v|vi|vii|viii|ix|x|xi|xii)\b", "", text)
    # Replace punctuation with space 
    text = re.sub(r"[^\w\s]", " ", text) 
    # Replace dashes (hyphen, en dash, em dash) with spaces to preserve word separation
    text = re.sub(r"[\u2014\u2013\-_()]", " ", text)
    # Replace multiple spaces with a single space
    text = re.sub(r"\s+", " ", text)
    # Strip leading and trailing spaces
    text = text.strip()
    # Tokenize the text
    text = word_tokenize(text)
    # Recreate the tokenized list but without NLTK stopwords
    filtered_sentence = []
    for w in text:
        if w not in stopwords.words('english'):
            filtered_sentence.append(w)
    return filtered_sentence

def preprocess_all_books(books_raw):
    for book in books_raw:
        cleaned_text = preprocess_text(book["text"])  # Clean the raw text
        book["text"] = cleaned_text  # Replace the raw text with the cleaned version