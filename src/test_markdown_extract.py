import unittest

from markdown_utils import extract_markdown_images, extract_markdown_links


class TestMarkdownExtractors(unittest.TestCase):
    def test_extract_markdown_images(self):
        text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_multiple_images(self):
        text = "Here ![a](http://x/a.png) and ![b](http://x/b.jpg)"
        matches = extract_markdown_images(text)
        self.assertListEqual(
            [("a", "http://x/a.png"), ("b", "http://x/b.jpg")], matches
        )

    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_links(text)
        self.assertListEqual(
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
            matches,
        )

    def test_links_do_not_match_images(self):
        text = "Mix ![img](http://x/i.png) and [link](http://x)"
        img = extract_markdown_images(text)
        link = extract_markdown_links(text)
        self.assertListEqual([("img", "http://x/i.png")], img)
        self.assertListEqual([("link", "http://x")], link)

    def test_no_matches(self):
        self.assertListEqual([], extract_markdown_images("no images here"))
        self.assertListEqual([], extract_markdown_links("no links here"))


if __name__ == "__main__":
    unittest.main()
