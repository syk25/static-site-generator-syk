import unittest

from markdown_utils import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_extract_title_happy(self):
        self.assertEqual(extract_title("# Hello"), "Hello")
        self.assertEqual(extract_title("#  Hello World  "), "Hello World")

    def test_extract_title_from_multiline(self):
        md = """
# Tolkien Fan Club

Some paragraph
"""
        self.assertEqual(extract_title(md), "Tolkien Fan Club")

    def test_no_h1_raises(self):
        with self.assertRaises(ValueError):
            extract_title("## Not h1\n#NoSpace\nNo header here")


if __name__ == '__main__':
    unittest.main()
