import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props_none(self):
        node = HTMLNode(tag="p", value="Hello")
        self.assertEqual(node.props_to_html(), "")

    def test_props_single(self):
        node = HTMLNode(tag="a", value="Link", props={"href": "https://example.com"})
        self.assertEqual(node.props_to_html(), ' href="https://example.com"')

    def test_props_multiple(self):
        node = HTMLNode(
            tag="a",
            value="Link",
            props={"href": "https://example.com", "target": "_blank"},
        )
        # Order should follow insertion order of dict; compare sets of substrings to be order-agnostic
        html = node.props_to_html()
        self.assertIn(' href="https://example.com"', html)
        self.assertIn(' target="_blank"', html)


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(), '<a href="https://www.google.com">Click me!</a>'
        )

    def test_leaf_value_required(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_no_tag_raw_text(self):
        node = LeafNode(None, "raw text")
        self.assertEqual(node.to_html(), "raw text")


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_parent_missing_tag_raises(self):
        child = LeafNode("p", "x")
        with self.assertRaises(ValueError):
            ParentNode(None, [child]).to_html()

    def test_parent_missing_children_raises(self):
        with self.assertRaises(ValueError):
            ParentNode("div", None).to_html()

    def test_nested_parent_multiple_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )


if __name__ == "__main__":
    unittest.main()
