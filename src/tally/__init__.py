"""Tally: count the words in a piece of text.

This is the practice project for the QUILL GitHub Practice repository. It is
small on purpose, and it has a known bug: see the issue "Word count is off by
one when text ends with a space".
"""

__version__ = "0.1.0"


def word_count(text):
    """Return how many words *text* holds.

    A word is anything between spaces. Hyphenated words, such as
    "screen-reader", count as one word.
    """
    if not text:
        return 0
    return len(text.replace("-", " ").split())


def character_count(text, include_spaces=True):
    """Return how many characters *text* holds."""
    if include_spaces:
        return len(text)
    return len(text.replace(" ", ""))


def summary(text):
    """Return a one-line summary, such as "3 words, 15 characters"."""
    words = word_count(text)
    characters = character_count(text)
    word_label = "word" if words == 1 else "words"
    character_label = "character" if characters == 1 else "characters"
    return f"{words} {word_label}, {characters} {character_label}"
