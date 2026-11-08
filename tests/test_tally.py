import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import tally  # noqa: E402


class WordCountTests(unittest.TestCase):
    def test_empty_text_has_no_words(self):
        self.assertEqual(tally.word_count(""), 0)

    def test_counts_simple_sentence(self):
        self.assertEqual(tally.word_count("the quick brown fox"), 4)

    def test_counts_hyphenated_words(self):
        self.assertEqual(tally.word_count("a screen-reader user"), 3)


class CharacterCountTests(unittest.TestCase):
    def test_counts_spaces_by_default(self):
        self.assertEqual(tally.character_count("a b"), 3)

    def test_can_leave_spaces_out(self):
        self.assertEqual(tally.character_count("a b", include_spaces=False), 2)


class SummaryTests(unittest.TestCase):
    def test_summary_uses_plurals(self):
        self.assertEqual(tally.summary("hello there"), "2 words, 11 characters")

    def test_summary_uses_singulars(self):
        self.assertEqual(tally.summary("a"), "1 word, 1 character")


if __name__ == "__main__":
    unittest.main()
