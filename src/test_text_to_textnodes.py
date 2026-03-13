import unittest

from textnode import TextNode, TextType, text_to_textnodes


class TestTextToTextNodes(unittest.TestCase):
    def test_full_example(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode(
                "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
            ),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertListEqual(expected, nodes)

    def test_only_text(self):
        self.assertListEqual(
            [TextNode("hello", TextType.TEXT)], text_to_textnodes("hello")
        )

    def test_ordering(self):
        # ensure processing images then links then formatting works
        text = "prefix ![i](u) mid [a](x) **b** _c_ `d` suffix"
        nodes = text_to_textnodes(text)
        expected_texts = [n.text for n in nodes]
        self.assertIn("i", expected_texts)
        self.assertIn("a", expected_texts)
        self.assertIn("b", expected_texts)
        self.assertIn("c", expected_texts)
        self.assertIn("d", expected_texts)


if __name__ == "__main__":
    unittest.main()
