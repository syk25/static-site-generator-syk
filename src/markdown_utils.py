import re
from typing import List, Tuple
from enum import Enum
import re
from htmlnode import ParentNode, LeafNode
from textnode import text_to_textnodes, text_node_to_html_node, TextNode, TextType


def extract_markdown_images(text: str) -> List[Tuple[str, str]]:
    """Return list of (alt, url) tuples for markdown images in `text`.

    Matches patterns like: ![alt text](http://example.com/image.png)
    """
    pattern = re.compile(r"!\[([^\]]*)\]\((.*?)\)")
    return pattern.findall(text)


def extract_markdown_links(text: str) -> List[Tuple[str, str]]:
    """Return list of (anchor, url) tuples for markdown links in `text`.

    Matches patterns like: [link text](http://example.com). Does not
    include image syntax (which starts with '!').
    """
    pattern = re.compile(r"(?<!\!)\[([^\]]+)\]\((.*?)\)")
    return pattern.findall(text)


def markdown_to_blocks(markdown: str) -> List[str]:
    """Split a markdown document into top-level blocks.

    Blocks are separated by one or more blank lines. Each returned block is
    stripped of leading/trailing whitespace and empty blocks are removed.
    """
    # Split on double-newline sequences. Keep simple: split on "\n\n".
    parts = markdown.split("\n\n")
    blocks = [p.strip() for p in parts]
    return [b for b in blocks if b]


class BlockType(Enum):
    HEADING = "heading"
    CODE_BLOCK = "code_block"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"
    PARAGRAPH = "paragraph"


def block_to_block_type(block: str) -> BlockType:
    """Return the BlockType for a given stripped markdown block string.

    Assumes `block` has no leading/trailing whitespace.
    """
    if not block:
        return BlockType.PARAGRAPH

    # Heading: starts with 1-6 '#' followed by a space
    if re.match(r"^#{1,6} ", block):
        return BlockType.HEADING

    # Multiline code block: starts with ```\n and ends with ```
    if block.startswith("```\n") and block.rstrip().endswith("```"):
        return BlockType.CODE_BLOCK

    lines = block.split("\n")

    # Quote block: every line starts with '>'
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    # Unordered list: every line starts with '- '
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    # Ordered list: every line starts with a number and '. ', and numbers start at 1 and increment
    ol_match = [re.match(r"^(\d+)\. ", line) for line in lines]
    if all(m is not None for m in ol_match):
        nums = [int(m.group(1)) for m in ol_match]
        # must start at 1 and increment by 1
        if nums == list(range(1, len(nums) + 1)):
            return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


def extract_title(markdown: str) -> str:
    """Extract the first H1 title from a markdown string.

    Looks for a line starting with a single '#' followed by a space.
    Returns the title text with surrounding whitespace stripped. Raises
    ValueError if no H1 is found.
    """
    for line in markdown.splitlines():
        m = re.match(r"^#\s+(.*)$", line)
        if m:
            return m.group(1).strip()
    raise ValueError("No H1 title found in markdown")


def text_to_children(text: str):
    """Convert inline markdown text into a list of HTMLNode children.

    Uses `text_to_textnodes` to get TextNode objects and converts each to
    an HTML node using `text_node_to_html_node`.
    """
    tn = text_to_textnodes(text)
    children = []
    for t in tn:
        children.append(text_node_to_html_node(t))
    return children


def markdown_to_html_node(markdown: str) -> ParentNode:
    """Convert a full markdown document string into a single ParentNode (div).

    This creates block-level HTML nodes and uses `text_to_children` for inline
    parsing. Code blocks are inserted without inline parsing.
    """
    blocks = markdown_to_blocks(markdown)
    block_nodes = []

    for block in blocks:
        btype = block_to_block_type(block)

        if btype == BlockType.HEADING:
            m = re.match(r"^(#{1,6})\s+(.*)", block)
            level = len(m.group(1))
            text = m.group(2).replace("\n", " ")
            block_nodes.append(ParentNode(f"h{level}", text_to_children(text)))

        elif btype == BlockType.CODE_BLOCK:
            # keep raw content between the triple backticks, including final newline
            if block.startswith("```") and block.endswith("```"):
                # capture content between opening ```\n and closing ```
                content = block[4:-3] if block.startswith("```\n") else block[3:-3]
            else:
                content = block
            # create <pre><code>content</code></pre>
            code_node = text_node_to_html_node(TextNode(content, TextType.CODE))
            block_nodes.append(ParentNode("pre", [code_node]))

        elif btype == BlockType.QUOTE:
            lines = block.split("\n")
            cleaned = [re.sub(r"^>\s?", "", l) for l in lines]
            # collapse intra-quote newlines into spaces
            joined = " ".join(cleaned)
            # render quote content directly inside blockquote (no inner <p>)
            block_nodes.append(ParentNode("blockquote", text_to_children(joined)))

        elif btype == BlockType.UNORDERED_LIST:
            items = [l[2:].replace("\n", " ") for l in block.split("\n")]
            lis = [ParentNode("li", text_to_children(item)) for item in items]
            block_nodes.append(ParentNode("ul", lis))

        elif btype == BlockType.ORDERED_LIST:
            items = [
                re.sub(r"^\d+\.\s+", "", l).replace("\n", " ")
                for l in block.split("\n")
            ]
            lis = [ParentNode("li", text_to_children(item)) for item in items]
            block_nodes.append(ParentNode("ol", lis))

        else:
            # paragraph: collapse internal newlines to spaces
            block_nodes.append(
                ParentNode("p", text_to_children(block.replace("\n", " ")))
            )

    return ParentNode("div", block_nodes)
