from typing import List, Optional, Dict


class HTMLNode:
    def __init__(
        self,
        tag: Optional[str] = None,
        value: Optional[str] = None,
        children: Optional[List["HTMLNode"]] = None,
        props: Optional[Dict[str, str]] = None,
    ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self) -> str:
        raise NotImplementedError()

    def props_to_html(self) -> str:
        if not self.props:
            return ""
        parts = []
        for k, v in self.props.items():
            parts.append(f' {k}="{v}"')
        return "".join(parts)

    def __repr__(self) -> str:
        return f"HTMLNode(tag={self.tag!r}, value={self.value!r}, children={self.children!r}, props={self.props!r})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props: Optional[Dict[str, str]] = None):
        # tag and value are required parameters (tag may be None)
        super().__init__(tag=tag, value=value, children=None, props=props)

    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("LeafNode must have a value")
        if self.tag is None:
            return self.value
        props_html = self.props_to_html()
        return f"<{self.tag}{props_html}>{self.value}</{self.tag}>"

    def __repr__(self) -> str:
        return f"LeafNode(tag={self.tag!r}, value={self.value!r}, props={self.props!r})"


class ParentNode(HTMLNode):
    def __init__(
        self,
        tag: Optional[str],
        children: Optional[List[HTMLNode]],
        props: Optional[Dict[str, str]] = None,
    ):
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self) -> str:
        if self.tag is None:
            raise ValueError("ParentNode must have a tag")
        if self.children is None:
            raise ValueError("ParentNode must have children")
        child_html = []
        for c in self.children:
            child_html.append(c.to_html())
        props_html = self.props_to_html()
        return f"<{self.tag}{props_html}>{''.join(child_html)}</{self.tag}>"

    def __repr__(self) -> str:
        return f"ParentNode(tag={self.tag!r}, children={self.children!r}, props={self.props!r})"
