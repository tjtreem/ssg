class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props is None or len(self.props) == 0:
            return ""
        
        result = ""
        for key, value in self.props.items():
            result += f' {key}="{value}"'

        return result

    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError("A value is required for LeafNode")
        if self.tag == None:
            return self.value

        attribute_strings = []
        
        if self.props:
            for key, value in self.props.items():
                attribute_strings.append(f'{key}="{value}"')

        attributes = " ".join(attribute_strings)
        attributes_part = " " + attributes if attributes else ""
        return f"<{self.tag}{attributes_part}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("ParentNode must contain a tag")
        if self.children == None:
            raise ValueError("Children are required for ParentNode")

        html =f"<{self.tag}"

        if self.props:
            for prop, value in self.props.items():
                html += f' {prop}="{value}"'

        html += ">"

        for child in self.children:
            html += child.to_html()

        html += f"</{self.tag}>"

        return html


def to_html(node):
    """Helper function that calls the to_html method on the given node."""
    return node.to_html()



        




    

