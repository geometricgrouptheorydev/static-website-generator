from enum import Enum
#Initial markdown parsing

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"
    # TABLE = "table" future feature!

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    #Blocks here are paragraph blocks; easier to parse markdown block by block
    return [block.strip() for block in blocks if block != ""]

def is_heading(block):
    #checks if the block is a heading, helper for block_to_block_type
    i = 0
    while i < len(block) and block[i] == '#':
        i += 1
    return 1 <= i <= 6 and i < len(block) and block[i] == ' '

def block_to_block_type(block):
    if is_heading(block):
        return BlockType.HEADING
    elif block.startswith("```") and block.endswith("```"): #markdown code syntax
        return BlockType.CODE
    lines = block.split("\n")
    if False not in [line.startswith(">") for line in lines]: #checks if each line starts with a >
        return BlockType.QUOTE
    elif False not in [line.startswith("-") for line in block.split("\n")]: #checks if each line starts with a -
        return BlockType.UNORDERED_LIST
    elif False not in [lines[i].startswith(f"{i+1}.") for i in range(0,len(lines))]: #cehcks if eahc line starts with 1., 2., 3., 3tc.
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH