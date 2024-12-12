# Sherlock Holmes Text Analysis

This project analyzes word usage in five Sherlock Holmes novels using text processing and data visualization techniques. The analysis includes word frequency, unique words, N-grams, TF-IDF scores, and co-occurrence heatmaps.

## Step-by-Step Breakdown
To see a full breakdown of the code as well as more analysis, see my accompanying Jupyter Notebook:

[Jupyter Notebook](https://github.com/chayre/word_frequency_analysis/blob/main/jupyter_notebook.ipynb)


![image](https://github.com/user-attachments/assets/1ecdcaec-bd0b-418a-ae0b-49ff4b86adff)

## Features
- **Text Preprocessing**: Tokenization, lemmatization, and cleaning using `NLTK` and `regex`.
- **Word Frequency Analysis**: Most common words visualized through word clouds and bar charts.
- **Unique Words**: Identification and visualization of unique words in each novel.
- **TF-IDF Analysis**: Heatmaps showing word importance across novels.
- **Co-occurrence Analysis**: Visualizing word pair frequencies in text.
- **N-gram Analysis**: Top bigrams identified and visualized for deeper insights.

## Data Source
The texts were sourced from [Project Gutenberg](https://www.gutenberg.org):
- *A Study in Scarlet*
- *The Valley of Fear*
- *The Sign of the Four*
- *The Hound of the Baskervilles*
- *The Adventures of Sherlock Holmes*

## Technologies Used
- **Python Libraries**:
  - Data collection: `URL Requests`
  - Data processing: `Pandas`, `NumPy`, `NLTK`
  - Visualization: `Matplotlib`, `Seaborn`, `WordCloud`
  - Utilities: `Requests`, `regex`, `itertools`
- **Data Formats**: JSON for intermediate storage.

## Project Structure
The codebase is modularized for clarity:
- **`data_collection.py`**: Functions for downloading and saving text data.
- **`data_preprocessing.py`**: Cleaning and tokenization.
- **`data_analysis.py`**: Word frequency, TF-IDF, and N-gram calculations.
- **`data_graphing.py`**: Visualizations including word clouds and heatmaps.

## Key Insights
- *Most Common Words*: Words like "man" and "Holmes" dominate the corpus.
- *Unique Words*: Proper nouns like "Baskerville" highlight novel-specific elements.
- *N-grams*: Phrases such as "Sherlock Holmes" and "last night" reveal thematic elements.
- *TF-IDF*: Words like "Moor" and "Douglas" distinguish specific novels.

## Visualizations
The project includes:
1. **Word Clouds**: Highlighting frequent words and unique words.
2. **Bar Charts**: Frequency and normalized frequency of top words and frequency of n-grams.
3. **Heatmaps**: TF-IDF Scores, co-occurrence of common words.
4. **Line charts**: For visualizing changes in mean word length over time.

Some visualizations:

![image](https://github.com/user-attachments/assets/b9025064-2045-4a29-a8ca-e59f09913795)
![image](https://github.com/user-attachments/assets/51103bbc-797a-4cff-9126-a5fa2d787a54)
![image](https://github.com/user-attachments/assets/f7d338f5-5a9f-4ed2-93e4-9f83b5a9059e)

## Assumptions and Limitations
- Removed uninteresting words like 'would', 'could', 'one', 'two' - however, these were some of the most common words
- The analysis focuses only on five novels, excluding short stories.
- The project assumes consistent formatting in Project Gutenberg texts.

## External References
- [WordCloud Masking Tutorial](https://medium.com/@m3redithw/wordclouds-with-python-c287887acc8b)
- Additional references: Python documentation and Stack Overflow for troubleshooting.

## Conclusion
This analysis provided insights into word usage patterns, unique phrases, and thematic elements in Sherlock Holmes novels. It demonstrates the power of computational text analysis in exploring literary works.
