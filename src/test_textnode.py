import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_equal_text(self):
        node = TextNode("Hello", TextType.BOLD)
        node1 = TextNode("World", TextType.BOLD)
        self.assertNotEqual(node, node1)

    def test_not_equal_text_type(self):
        node = TextNode("Hello", TextType.BOLD)
        node2 = TextNode("Hello", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_not_equal_url(self):
        node = TextNode("Click", TextType.LINK, "https://boot.dev")
        node2 = TextNode("Click", TextType.LINK, "https://google.com")
        self.assertNotEqual(node, node2)

    def test_equal_none_url(self):
        node = TextNode("Text", TextType.TEXT, None)
        node2 = TextNode("Text", TextType.TEXT, None)
        self.assertEqual(node, node2)

    def test_equal_text(self):
        node = TextNode("Robert", TextType.Text, None)
        node2 = TextNode("Robert", TextType.Text, None)
        self.assertEqual(node, node2)


if __name__ == "__main__":
    unittest.main()
