import requests
from bs4 import BeautifulSoup
import sys
import json


def word_freq_extract(word_frequency):
    # Access wordfrequency web-page
    url = 'https://www.wordfrequency.info/free.asp?s=y'
    try:
        response = requests.get(url)
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)
    soup = BeautifulSoup(response.text, 'lxml')
    table = soup.find_all('table')
    rows = table[3].find_all('tr')
    for i in range(4, len(rows)):
        tds = rows[i].find_all('td')
        values = [td.text for td in tds]
        word_frequency[int(values[0])] = {'word': values[1],
                                          'frequency': int(values[3])}
        if i == 5000:
            # The web-page contains records of 5000 words
            break

    if len(word_frequency) == 0:
        sys.exit("The word_freq_extract method has failed!")

    return word_frequency


def google_10k_words(word_no_swears):
    lines = []
    # Access Github raw contents web-page
    url = \
        'https://raw.githubusercontent.com/first20hours/google-10000-english/master/google-10000-english-no-swears.txt'
    try:
        response = requests.get(url)
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)
    soup = BeautifulSoup(response.text, 'lxml')
    lines = soup.text.split()
    for index, value in enumerate(lines):
        word_no_swears[index] = {'word': value, 'length': len(value)}

    if len(word_no_swears) == 0:
        sys.exit("The word_freq_extract method has failed!")

    return word_no_swears


def main():
    language = {}
    # Raw data of letter frequency
    # Reference: https://en.wikipedia.org/wiki/Letter_frequency
    letter_frequency = {
        'a': 8.497,
        'b': 1.492,
        'c': 2.202,
        'd': 4.253,
        'e': 11.162,
        'f': 2.228,
        'g': 2.015,
        'h': 6.094,
        'i': 7.546,
        'j': 0.153,
        'k': 1.292,
        'l': 4.025,
        'm': 2.406,
        'n': 6.749,
        'o': 7.507,
        'p': 1.929,
        'q': 0.095,
        'r': 7.587,
        's': 6.327,
        't': 9.356,
        'u': 2.758,
        'v': 0.978,
        'w': 2.560,
        'x': 0.150,
        'y': 1.994,
        'z': 0.077
    }

    # Parsed data from Word Frequency
    # Reference: https://www.wordfrequency.info/free.asp?s=y
    word_frequency = {}
    word_frequency = word_freq_extract(word_frequency)

    # Parsed data from google-10000-english-no-swears
    # Reference:
    # https://raw.githubusercontent.com/first20hours/google-10000-english/master/google-10000-english-no-swears.txt
    word_no_swears = {}
    word_no_swears = google_10k_words(word_no_swears)

    # Composed result is a nested dictionary
    language = {'letter_frequency': letter_frequency,
                'word_frequency': word_frequency,
                'word_no_swears': word_no_swears}

    # Save the result
    with open('language_data.json', 'w') as output_file:
        json.dump(language, output_file)


if __name__ == '__main__':
    main()
