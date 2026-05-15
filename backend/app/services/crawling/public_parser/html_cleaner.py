from __future__ import annotations

import html
import re
from dataclasses import dataclass, field
from html.parser import HTMLParser
from typing import Iterable


_WHITESPACE_RE = re.compile(r"\s+")
_VOID_TAGS = {
    "area",
    "base",
    "br",
    "col",
    "embed",
    "hr",
    "img",
    "input",
    "link",
    "meta",
    "param",
    "source",
    "track",
    "wbr",
}


@dataclass
class HtmlNode:
    tag: str
    attrs: dict[str, str] = field(default_factory=dict)
    parent: "HtmlNode | None" = None
    children: list["HtmlNode"] = field(default_factory=list)
    text_chunks: list[str] = field(default_factory=list)

    def text_content(self) -> str:
        chunks = list(self.text_chunks)
        for child in self.children:
            chunks.append(child.text_content())
        return normalize_text(" ".join(chunks))


class _TreeParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.root = HtmlNode("document")
        self._stack: list[HtmlNode] = [self.root]

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        node = HtmlNode(tag=tag.lower(), attrs={key.lower(): value or "" for key, value in attrs})
        node.parent = self._stack[-1]
        self._stack[-1].children.append(node)
        if tag.lower() not in _VOID_TAGS:
            self._stack.append(node)

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)
        if self._stack and self._stack[-1].tag == tag.lower():
            self._stack.pop()

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        while len(self._stack) > 1:
            node = self._stack.pop()
            if node.tag == tag:
                break

    def handle_data(self, data: str) -> None:
        text = normalize_text(data)
        if text:
            self._stack[-1].text_chunks.append(text)


def normalize_text(value: str | None) -> str:
    if value is None:
        return ""
    return _WHITESPACE_RE.sub(" ", html.unescape(str(value))).strip()


def extract_first_text(document: str, selector: str | None) -> str:
    nodes = select_nodes(document, selector)
    if not nodes:
        return ""
    return nodes[0].text_content()


def extract_all_text(document: str, selector: str | None, *, limit: int | None = None) -> list[str]:
    texts = [node.text_content() for node in select_nodes(document, selector)]
    filtered = [text for text in texts if text]
    return filtered[:limit] if limit is not None else filtered


def select_nodes(document: str, selector: str | None) -> list[HtmlNode]:
    selector = normalize_text(selector)
    if not selector:
        return []
    parser = _TreeParser()
    parser.feed(document or "")
    chain = [_parse_simple_selector(part) for part in selector.split() if part]
    if not chain:
        return []
    return [node for node in _walk(parser.root.children) if _matches_selector_chain(node, chain)]


def _walk(nodes: Iterable[HtmlNode]) -> Iterable[HtmlNode]:
    for node in nodes:
        yield node
        yield from _walk(node.children)


def _parse_simple_selector(selector: str) -> dict[str, str | None]:
    if selector.startswith("#"):
        return {"tag": None, "id": selector[1:], "class": None}
    if selector.startswith("."):
        return {"tag": None, "id": None, "class": selector[1:]}
    if "." in selector:
        tag, class_name = selector.split(".", 1)
        return {"tag": tag.lower() or None, "id": None, "class": class_name}
    return {"tag": selector.lower(), "id": None, "class": None}


def _matches_selector_chain(node: HtmlNode, chain: list[dict[str, str | None]]) -> bool:
    if not _matches_simple_selector(node, chain[-1]):
        return False
    cursor = node.parent
    for expected in reversed(chain[:-1]):
        while cursor is not None and not _matches_simple_selector(cursor, expected):
            cursor = cursor.parent
        if cursor is None:
            return False
        cursor = cursor.parent
    return True


def _matches_simple_selector(node: HtmlNode, selector: dict[str, str | None]) -> bool:
    tag = selector.get("tag")
    node_id = selector.get("id")
    class_name = selector.get("class")
    if tag and node.tag != tag:
        return False
    if node_id and node.attrs.get("id") != node_id:
        return False
    if class_name:
        classes = node.attrs.get("class", "").split()
        return class_name in classes
    return True

