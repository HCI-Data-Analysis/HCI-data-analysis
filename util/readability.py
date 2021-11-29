import re

import nltk

nltk.download('cmudict')


def get_syllables(paragraph):
    d = nltk.corpus.cmudict.dict()

    parsed = re.sub(r'[^\w\s]', '', paragraph)
    words = parsed.split(' ')
    count = 0
    for word in words:
        count += get_syllables_word(word, d)

    return count


def get_syllables_word(word, dict):
    try:
        return len(list(y for y in dict[word.lower()][0] if y[-1].isdigit()))
    except KeyError:
        return 1


def get_flesch_reading_ease(paragraph):
    """
    Perform the Flesch reading ease readability test on a given paragraph,
    implemented based on the algorithm given in:
    https://web.archive.org/web/20160712094308/http://www.mang.canterbury.ac.nz/writing_guide/writing/flesch.shtml
    Use the same link to determine what level of reading the paragraph falls under

    :param paragraph: Paragraph you want to analyze
    :return: Result
    """

    sentences = paragraph.split('.')
    if sentences[-1] == '':
        del sentences[-1]
    number_of_sentences = len(sentences)
    number_of_words = len(paragraph.split(' '))
    number_of_syllables = get_syllables(paragraph)

    try:
        flesch_reading_result = 206.835 - 1.015 * (number_of_words / number_of_sentences) - 84.6 * (
                number_of_syllables / number_of_words)
    except ZeroDivisionError:
        return 100

    return flesch_reading_result
