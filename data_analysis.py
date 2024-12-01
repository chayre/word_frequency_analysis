#Analysis functions
from collections import Counter

# Count most common words
def return_most_common(text, n):
    word_counts = Counter(text.split())
    most_common = word_counts.most_common(n)
    return most_common 