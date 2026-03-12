import unittest

from textnode import TextNode, TextType, split_nodes_image, split_nodes_link


class TestSplitNodesImageLink(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            ],
            new_nodes,
        )

    def test_mixed_image_and_link(self):
        node = TextNode(
            "Start ![i](http://x/i.png) middle [a](http://x) end",
            TextType.TEXT,
        )
        # first split images, then links (order matters)
        nodes_after_images = split_nodes_image([node])
        result = split_nodes_link(nodes_after_images)
        self.assertListEqual(
            [
                TextNode("Start ", TextType.TEXT),
                TextNode("i", TextType.IMAGE, "http://x/i.png"),
                TextNode(" middle ", TextType.TEXT),
                TextNode("a", TextType.LINK, "http://x"),
                TextNode(" end", TextType.TEXT),
            ],
            result,
        )

    def test_preserve_non_text(self):
        bold = TextNode("b", TextType.BOLD)
        nodes = [bold, TextNode("plain [x](y)", TextType.PLAIN)]
        self.assertListEqual(nodes, split_nodes_link(nodes))
        self.assertListEqual(nodes, split_nodes_image(nodes))

    def test_no_matches_returns_same(self):
        node = TextNode("no images or links here", TextType.TEXT)
        self.assertListEqual([node], split_nodes_image([node]))
        self.assertListEqual([node], split_nodes_link([node]))


if __name__ == "__main__":
    unittest.main()
