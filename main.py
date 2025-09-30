from deep_translator import GoogleTranslator
from langdetect import detect
from textblob import TextBlob
import ru_local as ru

def count_syllables_russian(word):

    """
    Counts the number of syllables in a text (for Russian).

    Args:
    word(str): The word to split into syllables.

    Returns:
    int: Number of syllables.
    """

    word = word.lower()
    vowels = "аеёиоуыэюя"
    return sum(1 for char in word if char in vowels)


def count_syllables_english(word):

    """
    Counts the number of syllables in a text (for English)
    Args:
    word(str): The word to split into syllables.

    Returns:
    int: Number of syllables.
    """

    word = word.lower()
    vowels = "aeiouy"
    count = 0

    if word[0] in vowels:
        count += 1

    for i in range(1, len(word)):
        if word[i] in vowels and word[i - 1] not in vowels:
            count += 1

    if word[-1] == "e" and count > 1:
        count -= 1

    return max(1, count)


def simple_split_sentences(text):

    """
    Removes all unnecessary characters between sentences and replaces them with spaces (dashes and hyphens are included).
    Args:
    text(str): Text to split.

    Returns:
    list: List of split sentences.
    """

    text = text.replace("...", "…")
    sentence_endings = ".?!…"
    all_sentences = []
    current_sentence = ""

    for char in text:
        current_sentence += char
        if char in sentence_endings:
            all_sentences.append(current_sentence.strip())
            current_sentence = ""

    if current_sentence:
        all_sentences.append(current_sentence.strip())

    sentences = []
    current_sentence = all_sentences[0]

    for s in range(1, len(all_sentences)):
        next_sentence = all_sentences[s]
        first_alpha = None

        for char in next_sentence:
            if char.isalpha():
                first_alpha = char
                break

        if first_alpha.isupper():
            sentences.append(current_sentence)
            current_sentence = next_sentence
        else:
            current_sentence += " " + next_sentence

    if current_sentence:
        sentences.append(current_sentence)

    return sentences


def simple_split_words(text):

    """
    Removes all characters between words and replaces them with spaces, counting the number of words.
    Args:
    text(str): Text to split into words.

    Returns:
    list: List of words.
    """

    for char in text:
        if not char.isalpha() and char != "-":
            text = text.replace(char, " ")

    text = text.replace(" - ", " ")
    words = text.split()
    return words

def main(text):

    """
    The function displays the final result on the screen
    """

    sentences = simple_split_sentences(text)
    words = simple_split_words(text)
    num_sentences = len(sentences)
    num_words = len(words)
    language = detect(text)

    total_syllables = 0
    for word in words:
        if language == "ru":
            total_syllables += count_syllables_russian(word)
        else:
            total_syllables += count_syllables_english(word)

    avg_sentence_length = num_words / num_sentences
    avg_syllables_per_word = total_syllables / num_words

    if language == "ru":
        flesch_index = 206.835 - 1.3 * avg_sentence_length - 60.1 * avg_syllables_per_word
    else:
        flesch_index = 206.835 - 1.015 * avg_sentence_length - 84.6 * avg_syllables_per_word


    if flesch_index > 80:
        interpretation = ru.EASY_TEXT_ELEMENTARY
    elif flesch_index > 50:
        interpretation = ru.EASY_TEXT_MIDDLE
    elif flesch_index > 25:
        interpretation = ru.ALRIGHT
    else:
        interpretation = ru.THE_HECK_IS_THIS


    if language != "en":
        translator = GoogleTranslator()
        translated_text = translator.translate(text)
        translated_blob = TextBlob(translated_text)
        sentiment = translated_blob.sentiment
    else:
        blob = TextBlob(text)
        sentiment = blob.sentiment

    polarity = sentiment.polarity
    subjectivity = sentiment.subjectivity * 100

    if polarity > 0.1:
        tone = ru.POSITIVE
    elif polarity < -0.1:
        tone = ru.NEGATIVE
    else:
        tone = ru.NEUTRAL

    print(f"{ru.SENTENCES} {num_sentences}")
    print(f"{ru.WORDS} {num_words}")
    print(f"{ru.SYLLABLES} {total_syllables}")
    print(f"{ru.APR_LENGTH_SENTENCE} {avg_sentence_length:.4f}")
    print(f"{ru.APR_LENGTH_WORDS} {avg_syllables_per_word:.4f}")
    print(f"{ru.FLESCH_INDEX} {flesch_index:.4f}")
    print(interpretation)
    print(f"{ru.TONE} {tone}")
    print(f"{ru.OBJECTIVITY} {100 - subjectivity:.1f}%")


if __name__ == "__main__":
    text = input(ru.ENTER_TEXT)
    main(text)
