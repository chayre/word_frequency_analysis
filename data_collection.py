# Assumptions: all text files from Project Guntenberg begin with an introductory statement (Followed by * * *, after which the text of the book begins) and 
# are concluded with an ending statement (which is preceded by * * *, similarly). I remove these Project Gutenberg statements during cleaning. 
# However, I do not remove some details which would be found in a book such as table of contents; I assume this to be part of the text.
# I also assume that Project Gutenberg text files begin with a title, author, and language section. I use this to construct the metadata in my JSON.
# Only downloading the four Sherlock Holmes novels and the most popular collection of Sherlock Holmes short stories

import requests # Note -- external package

# URL request; return plain text if successful 
def download_book(url):
    response = requests.get(url)
    if response.status_code == 200: # HTTP status code for OK
        return response.text
    else:
        print(f"Failed to download {url}")
        return ""

# Function to save the text to a file
def save_to_file(text, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(text)
    print(f"File saved to {file_path}")

scarlet_book = download_book("https://www.gutenberg.org/cache/epub/244/pg244.txt") # A Study in Scarlet raw text
valley_book = download_book("https://www.gutenberg.org/cache/epub/3289/pg3289.txt") # The Valley of Fear raw text
sign_book = download_book("https://www.gutenberg.org/cache/epub/2097/pg2097.txt") # The Sign of the Four raw text
hound_book = download_book("https://www.gutenberg.org/cache/epub/2852/pg2852.txt") # The Hound of the Baskerviles raw text
adventures_book = download_book("https://www.gutenberg.org/cache/epub/1661/pg1661.txt") # The Adventures of Sherlock Holmes raw text

holmes_collection_raw = (scarlet_book, valley_book, sign_book, hound_book, adventures_book)

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

