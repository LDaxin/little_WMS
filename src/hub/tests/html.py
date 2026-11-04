"""Small helpers for asserting the rendered DOM structure in tests."""
from html.parser import HTMLParser

_VOID = {"input", "br", "img", "meta", "link", "hr"}


class _Nesting(HTMLParser):
    def __init__(self, container_id):
        super().__init__()
        self.container_id = container_id
        self.stack = []
        self.found = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag not in _VOID:
            self.stack.append(attrs.get("id"))
        if attrs.get("id") and self.container_id in self.stack:
            self.found.append(attrs["id"])

    def handle_endtag(self, tag):
        if tag not in _VOID and self.stack:
            self.stack.pop()


def ids_inside(content, container_id):
    """Ids of elements nested inside ``#<container_id>`` (rough HTML nesting)."""
    parser = _Nesting(container_id)
    parser.feed(content)
    return parser.found
