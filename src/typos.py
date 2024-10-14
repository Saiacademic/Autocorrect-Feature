# Common typo dictionary
TYPO_DICT = {
    'fir': 'for',
    'hte': 'the',
    'recieve': 'receive',
    'adress': 'address',
    'teh': 'the',
    'beleive': 'believe',
    'occurence': 'occurrence'
    # Add more common typos here
}

def correct_typos(text):
    """
    Correct common typos in the given text.
    """
    words = text.split()
    corrected_words = [TYPO_DICT.get(word, word) for word in words]
    return ' '.join(corrected_words)
