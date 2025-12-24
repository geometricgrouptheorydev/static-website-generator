import re
from blocks import BlockType, markdown_to_blocks, block_to_block_type, is_heading
from htmlnode import LeafNode, ParentNode
from splitter import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node

def heading_level(heading): #helper function to find the heading type
    return sum( 1 for i in range(0,6) if heading[i] == "#" )

type_to_tags = {
    # this is a dictionary that maps blocktypes to quadruple: (outer tag, inner tag, can it have children?, (sub)string to strip)
    BlockType.PARAGRAPH: ("p", None, True, r"^\s*"), #remove leading whitespace
    BlockType.QUOTE: ("blockquote", None, True, r"^>\s*"), #remove leading > + whitespace
    BlockType.CODE: ("pre", None, False, "```"), #remove leading and ending ``` only, despite this markdown_to_html_node will use string slicing anyway lol
    BlockType.UNORDERED_LIST: ("ul", "li", True, r"^-\s*"), #remove leading > + whitespace
    BlockType.ORDERED_LIST: ("ol", "li", True, r"^\d.\s*"), #remove leading number + dot
    BlockType.HEADING: ("h", None, True, r"^#{1,6}\s*") #primary tag is h here but the number next to the h will be added later
    }

def markdown_to_html_node(markdown):
    parents = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        taipe = block_to_block_type(block) #"taipe" because "type" is a python keyword
        tags = type_to_tags[taipe]
        # setting the parent node
        if not tags[2]: #no child node, so is a code block
            filtered_block = block[4:-3]
            child = text_node_to_html_node(TextNode(filtered_block, TextType.CODE))
            parents.append(ParentNode("pre", [child]))
            continue
        elif tags[0] == "h": #we have a heading
            tags = (f"h{heading_level(block)}", None, True, r"^#{1,6}\s*") #str stripped are the begining #s and whitespaces right after. 
        unfiltered_lines = block.split("\n")
        lines = [re.sub(tags[3], "", line) for line in unfiltered_lines]
        if tags[1] == None: #not a list
            filtered_block = " ".join(lines)
            children = [text_node_to_html_node(node) for node in text_to_textnodes(filtered_block)]
        else: #we've got a list; we have grandchildren!
            grandchildren = []
            for line in lines:
                grandchildren.append([text_node_to_html_node(node) for node in text_to_textnodes(line)])
            children = [ParentNode(tags[1], grandchildren[i]) for i in range(0,len(grandchildren))]
        parents.append(ParentNode(tags[0], children))
    return ParentNode("div", parents)

def extract_title(markdown):
    search = re.search(r"(?<=[^#]# )[^#+].+(?=\n)", " " + markdown) #regex looks if there is exactly one # and a space
    return search.group(0).strip() if search else ""