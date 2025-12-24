from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
	TEXT = None
	BOLD =  "b"
	ITALIC = "i"
	CODE = "code"
	LINK = "a"
	IMAGE = "img"
	STRIKETHROUGH = "s"
	SUPERSCRIPT = "sup"
	SUBSCRIPT = "sub"

	@property
	def label(self):
		# pretty display name
		return self.name.lower() if self is not TextType.TEXT else "text"

class TextNode:
	def __init__(self, text, text_type, url = None):
		self.text = text
		self.text_type = text_type
		self.url = url

	def __eq__(self, other):
		return self.text == other.text and self.text_type == other.text_type and self.url == other.url

	def __repr__(self):
		return f'TextNode("{self.text}",{self.text_type.label},{self.url})'

def text_node_to_html_node(text_node):
	if text_node.text_type not in set(TextType):
		raise ValueError(f"Invalid TextType: {text_node.text_type!r}")
	elif text_node.text_type == TextType.TEXT:
		return LeafNode(None, text_node.text)
	elif text_node.text_type == TextType.IMAGE:
		props = {"src": text_node.url, "alt": text_node.text}
		return LeafNode("img", "", props)
	
	props = None
	if text_node.text_type == TextType.LINK:
		props = {"href": text_node.url}
	tag = text_node.text_type.value
	return LeafNode(tag, text_node.text, props)