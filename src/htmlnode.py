class HTMLNode: #its children classes LeafNode and ParentNode will be used
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag, self.value, self.children, self.props = tag, value, children, props

    def to_html(self):
        raise NotImplementedError("to_html method not implemented (use a subclass)")
    
    def props_to_html(self):
        return  "".join([f' {key}="{self.props[key]}"' for key in self.props]) if self.props is not None else ""
    
    def __repr__(self):
        return f"HTMLNode({self.tag},{self.value}, children: {self.children},props: {self.props})"

class LeafNode(HTMLNode): #HTML tags with no subtags
    def __init__(self, tag, value, props = None):
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes must have a value.")
        elif self.tag is None: #for leaf nodes that do not hold a tag, to be used as a child to certain parent nodes such as bold and italic
            return f"{self.value}" 
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        
class ParentNode(HTMLNode): #HTML nodes that holds sub-nodes
    def __init__(self, tag, children, props = None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("All parent nodes must have a tag")
        elif self.children is None:
            raise ValueError("All parent nodes must have children")
        else:
            return f"<{self.tag}>" + "".join([child.to_html() for child in self.children]) + f"</{self.tag}>"