"""Process the raw data so that it is ready for textual analysis"""
import re
import NLTK

#stopwords = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves", #"you", "your", "yours", "yourself", "yourselves", "he", "him", "his", #"himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", #"them", "their", "theirs", "themselves", "what", "which", "who", "whom", #"this", "that", "these", "those", "am", "is", "are", "was", "were", "be", #"been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", #"a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", #"of", "at", "by", "for", "with", "about", "against", "between", "into", #"through", "during", "before", "after", "above", "below", "to", "from", "up", #"down", "in", "out", "on", "off", "over", "under", "again", "further", "then", #"once", "here", "there", "when", "where", "why", "how", "all", "any", "both", #"each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", #"only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", #"just", "dont", "should", "now", "shouldnt", "wont", "cant", "havent", "ii", #"iii", "iv", "v", "vi", "vii", "viii", "ix", "x", "xi", "xii"]

def process_text(text):
    """Convert raw text to processed text."""
    # Remove the introductory Project Gutenberg text (before the book starts)
    text = re.sub(r"^.*?( \*\*\*)", "", text, flags=re.DOTALL)
    # Remove the end Project Gutenberg text (after the book ends)
    text = re.sub(r"(END OF THE PROJECT GUTENBERG EBOOK.*)", "", text, flags=re.DOTALL)
    # Remove digits
    text = re.sub(r"\d+", "", text)
     # Remove apostrophes
    text = text.replace("'", "")
    text = text.replace("’", "") # Accounts for funky ’, which differs from regular apostrophe, '
    # Replace punctuation with space 
    text = re.sub(r"[^\w\s]", " ", text) 
    # Replace dashes (hyphen, en dash, em dash) with spaces to preserve word separation
    text = re.sub(r"[\u2014\u2013\-_()]", " ", text)
    # Remove stopwords
    stopwords_pattern = r'\b(?:' + '|'.join(map(re.escape, stopwords)) + r')\b'
    text = re.sub(stopwords_pattern, "", text, flags=re.IGNORECASE)
    # Replace multiple spaces with a single space
    text = re.sub(r"\s+", " ", text)
    # Strip leading and trailing spaces
    text = text.strip()
    # Make all text lower-case
    text = text.lower()
    return text

def process_all_books(books_raw):
    for book in books_raw:
        cleaned_text = process_text(book["text"])  # Clean the raw text
        book["text"] = cleaned_text  # Replace the raw text with the cleaned version