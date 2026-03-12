import unittest

from markdown_utils import markdown_to_blocks


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_trims_and_removes_empty(self):
        md = "\n\n  a block  \n\n\n   \n b\n\n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["a block", "b"])  


if __name__ == "__main__":
    unittest.main()
