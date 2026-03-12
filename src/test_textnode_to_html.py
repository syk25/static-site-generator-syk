import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNodeToHtml(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("bold me", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "bold me")

    def test_italic(self):
        node = TextNode("em", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")

    def test_code(self):
        # CODE may be added to enum; if not present this will still work if TextType.CODE exists
        if hasattr(TextType, "CODE"):
            node = TextNode("x = 1", TextType.CODE)
            html_node = text_node_to_html_node(node)
            self.assertEqual(html_node.tag, "code")

    def test_link(self):
        node = TextNode("click", TextType.LINK, "https://example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.props.get("href"), "https://example.com")

    def test_image(self):
        node = TextNode("alt text", TextType.IMAGE, "https://img.example/logo.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props.get("src"), "https://img.example/logo.png")
        self.assertEqual(html_node.props.get("alt"), "alt text")

    def test_unsupported_raises(self):
        class Dummy:
            pass

        # craft a TextNode-like with unknown type
        node = TextNode("x", TextType.PLAIN)
        # PLAIN maps to TEXT behavior; create a fake type to force failure
        node.text_type = Dummy()
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)


if __name__ == "__main__":
    unittest.main()
