from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    #input: list of textnodes, a markdown delimiter, and the texttype of each delimiter
    new_nodes = []
    for node in old_nodes:
        node_text_type = node.text_type
        split_text = node.text.split(delimiter)
        if len(split_text) % 2 == 0:
            raise SyntaxError("Invalid Markdown Syntax; either an extra delimiter was added or one is missing")
        use_node_text_type = True
        for text in split_text:
            current_text_type = node_text_type if use_node_text_type else text_type
            use_node_text_type = not use_node_text_type
            if text != "":
                new_nodes.append(TextNode(text, current_text_type))
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type in [TextType.IMAGE, TextType.LINK]:
            new_nodes.append(node)
            continue
        split_text = re.split(r"(!\[[^\[\]]*\]\([^\(\)]*\))", node.text)
        image_data = extract_markdown_images(node.text)
        for i in range(0, len(split_text)):
            if split_text[i] != "":
                if i%2 == 0:
                    new_nodes.append(TextNode(split_text[i], node.text_type))
                else:
                    new_nodes.append(TextNode(image_data[(i-1)//2][0], TextType.IMAGE, image_data[(i-1)//2][1]))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type in [TextType.IMAGE, TextType.LINK]:
            new_nodes.append(node)
            continue
        split_text = re.split(r"((?<!!)\[[^\[\]]*\]\([^\(\)]*\))", node.text)
        link_data = extract_markdown_links(node.text)
        for i in range(0, len(split_text)):
            if split_text[i] != "":
                if i%2 == 0:
                    new_nodes.append(TextNode(split_text[i], node.text_type))
                else:
                    new_nodes.append(TextNode(link_data[(i-1)//2][0], TextType.LINK, link_data[(i-1)//2][1]))
    return new_nodes

def text_to_textnodes(text): #Note: does not support nested delimiters yet!
    nodes = [TextNode(text, TextType.TEXT)] #The whole text is set under a textnode but we split those below
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC) #We want to support both italic syntaxes
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_delimiter(nodes, "~~", TextType.STRIKETHROUGH)
    nodes = split_nodes_delimiter(nodes, "^", TextType.SUPERSCRIPT)
    nodes = split_nodes_delimiter(nodes, "~", TextType.SUBSCRIPT)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes