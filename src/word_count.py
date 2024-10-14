def count_words(text):
    """
    Counts occurrences of each word in the given text.
    Returns a dictionary of word counts.
    """
    words = text.split()
    word_counts = {}
    for word in words:
        word_counts[word] = word_counts.get(word, 0) + 1
    return word_counts
