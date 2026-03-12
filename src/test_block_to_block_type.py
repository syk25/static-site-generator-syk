import unittest

from markdown_utils import BlockType, block_to_block_type


class TestBlockToBlockType(unittest.TestCase):
    def test_heading_levels(self):
        self.assertEqual(block_to_block_type('# Heading'), BlockType.HEADING)
        self.assertEqual(block_to_block_type('###### Small'), BlockType.HEADING)

    def test_code_block(self):
        md = "```\nprint('hi')\n```"
        self.assertEqual(block_to_block_type(md), BlockType.CODE_BLOCK)

    def test_quote(self):
        block = "> a quote\n> continued"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_unordered_list(self):
        block = "- item one\n- item two\n- item three"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_ordered_list_valid(self):
        block = "1. first\n2. second\n3. third"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_ordered_list_invalid_numbers(self):
        # not starting at 1
        block = "2. first\n3. second"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_non_sequential(self):
        block = "1. one\n3. three"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_mixed_lines_paragraph(self):
        block = "- item\nNot a list"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_empty_block(self):
        self.assertEqual(block_to_block_type(''), BlockType.PARAGRAPH)


if __name__ == '__main__':
    unittest.main()
