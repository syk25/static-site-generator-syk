from enum import Enum
from typing import Optional
import re


class TextType(Enum):
    PLAIN = "plain"
    LINK = "link"
    IMAGE = "image"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    TEXT = "text"
    Text = "text"


class TextNode:
    def __init__(self, text: str, text_type: TextType, url: Optional[str] = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if not isinstance(other, TextNode):
            return False
        return (
            self.text == other.text and
            self.text_type == other.text_type and
            self.url == other.url       
        )
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    

def text_node_to_html_node(text_node: TextNode):
    from htmlnode import LeafNode

    t = text_node.text_type
    if t == TextType.TEXT or t == TextType.PLAIN:
        return LeafNode(None, text_node.text)
    if t == TextType.BOLD:
        return LeafNode("b", text_node.text)
    if t == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    if t == TextType.__dict__.get("CODE"):
        return LeafNode("code", text_node.text)
    # handle CODE if present in enum
    if hasattr(TextType, "CODE") and t == TextType.CODE:
        return LeafNode("code", text_node.text)
    if t == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    if t == TextType.IMAGE:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})

    raise ValueError(f"Unsupported TextType: {t}")


def split_nodes_delimiter(old_nodes, delimiter, text_type: TextType):
    """Split text nodes in `old_nodes` by `delimiter` and mark the
    text between delimiters with `text_type`.

    Args:
        old_nodes: list of TextNode
        delimiter: string delimiter to split on (e.g. "`", "**", "_")
        text_type: TextType to assign to text found between delimiters

    Returns:
        list of TextNode with TEXT nodes split and other node types preserved.

    Raises:
        ValueError: if an unmatched delimiter is found inside a TEXT node.
    """
    new_nodes = []
    for node in old_nodes:
        # only attempt to split plain/text nodes
        if not isinstance(node, TextNode) or node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        parts = node.text.split(delimiter)
        occurrences = len(parts) - 1
        if occurrences == 0:
            new_nodes.append(node)
            continue

        # if there's an odd number of delimiters, that's unmatched
        if occurrences % 2 != 0:
            raise ValueError(f"Unmatched delimiter '{delimiter}' in text: {node.text}")

        # build alternating TEXT and target type nodes
        for i, part in enumerate(parts):
            if part == "":
                # keep empty segments to preserve positions (allows leading/trailing delimiters)
                text_part = ""
            else:
                text_part = part

            if i % 2 == 0:
                # outside delimiter -> TEXT
                if text_part != "":
                    new_nodes.append(TextNode(text_part, TextType.TEXT))
                else:
                    # append empty TEXT node to preserve structure
                    new_nodes.append(TextNode(text_part, TextType.TEXT))
            else:
                new_nodes.append(TextNode(text_part, text_type))

    return new_nodes


def split_nodes_image(old_nodes):
    """Split markdown image syntax in TEXT nodes into TEXT and IMAGE nodes.

    Looks for patterns like: ![alt](url)
    """
    new_nodes = []
    pattern = re.compile(r'!\[([^\]]*)\]\((.*?)\)')

    for node in old_nodes:
        if not isinstance(node, TextNode) or node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        last = 0
        found = False
        for m in pattern.finditer(text):
            found = True
            if m.start() > last:
                new_nodes.append(TextNode(text[last:m.start()], TextType.TEXT))
            alt = m.group(1)
            url = m.group(2)
            new_nodes.append(TextNode(alt, TextType.IMAGE, url))
            last = m.end()

        if not found:
            new_nodes.append(node)
        else:
            if last < len(text):
                new_nodes.append(TextNode(text[last:], TextType.TEXT))

    return new_nodes


def split_nodes_link(old_nodes):
    """Split markdown link syntax in TEXT nodes into TEXT and LINK nodes.

    Looks for patterns like: [anchor](url) but does not match images.
    """
    new_nodes = []
    pattern = re.compile(r'(?<!\!)\[([^\]]+)\]\((.*?)\)')

    for node in old_nodes:
        if not isinstance(node, TextNode) or node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        last = 0
        found = False
        for m in pattern.finditer(text):
            found = True
            if m.start() > last:
                new_nodes.append(TextNode(text[last:m.start()], TextType.TEXT))
            anchor = m.group(1)
            url = m.group(2)
            new_nodes.append(TextNode(anchor, TextType.LINK, url))
            last = m.end()

        if not found:
            new_nodes.append(node)
        else:
            if last < len(text):
                new_nodes.append(TextNode(text[last:], TextType.TEXT))

    return new_nodes


def text_to_textnodes(text: str):
    """Convert raw markdown-like `text` into a list of TextNode objects.

    Uses the splitter helpers in a specific order to handle images,
    links, bold, italic, and code inline markers.
    """
    nodes = [TextNode(text, TextType.TEXT)]
    # images and links first (bracket syntax)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    # formatting delimiters; order matters
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)

    return nodes




