import unittest

from textnode import TextNode, TextType, split_nodes_delimiter


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_backtick_single(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.__dict__.get("CODE", TextType.TEXT))
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.__dict__.get("CODE", TextType.TEXT)),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_bold_double_star(self):
        node = TextNode("Make this **bold** now", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("Make this ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" now", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_multiple_occurrences(self):
        node = TextNode("a `b` c `d` e", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.__dict__.get("CODE", TextType.TEXT))
        expected = [
            TextNode("a ", TextType.TEXT),
            TextNode("b", TextType.__dict__.get("CODE", TextType.TEXT)),
            TextNode(" c ", TextType.TEXT),
            TextNode("d", TextType.__dict__.get("CODE", TextType.TEXT)),
            TextNode(" e", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_unmatched_raises(self):
        node = TextNode("This has an `unmatched code", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", TextType.__dict__.get("CODE", TextType.TEXT))

    def test_preserve_non_text(self):
        bold_node = TextNode("bold", TextType.BOLD)
        nodes = [bold_node, TextNode("plain`, not matched", TextType.PLAIN)]
        # only TEXT nodes are split; none in input are TEXT so result should match input
        new_nodes = split_nodes_delimiter(nodes, "`", TextType.__dict__.get("CODE", TextType.TEXT))
        self.assertEqual(new_nodes, nodes)


if __name__ == "__main__":
    unittest.main()
