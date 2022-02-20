import requests
from bs4 import BeautifulSoup
import sys

languages = {1: 'Arabic',
             2: 'German',
             3: 'English',
             4: 'Spanish',
             5: 'French',
             6: 'Hebrew',
             7: 'Japanese',
             8: 'Dutch',
             9: 'Polish',
             10: 'Portuguese',
             11: 'Romanian',
             12: 'Russian',
             13: 'Turkish'}


def input_word():
    print('Type the word you want to translate:')
    word = input()
    return word


def create_url(lang_1, lang_2, word):
    url = 'https://context.reverso.net/translation/'
    return f'{url}{lang_1}-{lang_2}/{word}'


def get_words(s):
    words_raw = s.select("#translations-content .translation")
    words = [word.text.strip() for word in words_raw]
    return words


def get_sentences(s):
    sentences_raw = s.select("#examples-content .example .text")
    sentences = [sentence.text.strip() for sentence in sentences_raw]
    return sentences


def write_to_file(f_name, lst):
    with open(f_name, 'w', encoding='utf-8') as fh:
        fh.write('\n'.join(lst))


def read_from_file(f_name):
    with open(f_name, encoding='utf-8') as fh:
        for line in fh:
            print(line.strip())


def get_request(lang_or, lang_tr, word):
    trans_url = create_url(lang_or, lang_tr, word)
    user_agent = 'Mozilla/5.0'
    try:
        r = requests.get(trans_url, headers={'User-Agent': user_agent})
    except requests.exceptions.ConnectionError:
        print('Something wrong with your internet connection')
        return None
    else:
        if r.status_code == 200:
            return r
        print(f'Sorry, unable to find {word}')
        return None


def translator_manager(lang_or, lang_tr, word):
    r = get_request(lang_or, lang_tr, word)
    if not r:
        sys.exit()
    soup = BeautifulSoup(r.content, "html.parser")
    words = get_words(soup)
    sentences = get_sentences(soup)
    return words, sentences


def pretty_trans_result_one_lang(lang, words, sentences):
    result = list()
    result.append(f'{lang.title()} Translations:')
    if len(words) > 5:
        result.extend(words[:5])
    else:
        result.extend(words)
    result.append('')
    result.append(f'{lang.title()} Examples:')
    if len(sentences) > 10:
        sentences = sentences[:10]
    for i in range(0, len(sentences)-1, 2):
        result.append(sentences[i])
        result.append(sentences[i + 1])
        result.append('')
    return result


def pretty_trans_result_multi_lang(lang, words, sentences):
    result = list()
    result.append(f'{lang.title()} Translations:')
    result.append(words[0])
    result.append('')
    result.append(f'{lang.title()} Examples:')
    result.append(sentences[0])
    result.append(sentences[1])
    result.append('\n')
    return result


def is_language_ok(lang):
    if lang.title() in languages.values():
        return True
    return False


if __name__ == '__main__':
    args = sys.argv
    if not is_language_ok(args[1]):
        print(f"Sorry, the program doesn't support {args[1]}")
        sys.exit()
    if args[2] != 'all' and not is_language_ok(args[2]):
        print(f"Sorry, the program doesn't support {args[2]}")
        sys.exit()
    language_or = args[1]
    word_to_trans = args[3]    
    file_name = f'{word_to_trans}.txt'
    translation_result = []
    if args[2] != 'all':
        language_tr = args[2]
        words_trans, sentences_trans = translator_manager(language_or, language_tr, word_to_trans)
        translation_result = pretty_trans_result_one_lang(language_tr, words_trans, sentences_trans)
    else:
        for num in range(1, 14):
            language_tr = languages[num].lower()
            if language_tr == language_or:
                continue
            words_trans, sentences_trans = translator_manager(language_or, language_tr, word_to_trans)
            translation_result.extend(pretty_trans_result_multi_lang(language_tr, words_trans, sentences_trans))
    write_to_file(file_name, translation_result)
    read_from_file(file_name)
