import unittest

from src.htmlnode import HTMLNode, LeafNode, ParentNode



class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_empty(self):
        # Test with empty or None props
        node = HTMLNode(props=None)
        self.assertEqual(node.props_to_html(), "")
    
        node = HTMLNode(props={})
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_single_prop(self):
        # Test with a single property
        node = HTMLNode(props={"href": "https://www.example.com"})
        self.assertEqual(node.props_to_html(), ' href="https://www.example.com"')

    def test_props_to_html_multiple_props(self):
        # Test with multiple properties
        node = HTMLNode(props={
            "href": "https://www.example.com",
            "target": "_blank",
            "class": "link"
     })
    
        # Since dictionaries don't guarantee order, we need to check for all properties
        # without being concerned about their order
        result = node.props_to_html()
        self.assertIn(' href="https://www.example.com"', result)
        self.assertIn(' target="_blank"', result)
        self.assertIn(' class="link"', result)
        self.assertEqual(len(result), len(' href="https://www.example.com" target="_blank" class="link"'))


class TestLeafNode(unittest.TestCase):
    def test_leafnode_basic(self):
        node = LeafNode("p", "Hello world")
        self.assertEqual(node.to_html(), "<p>Hello world</p>")

    def test_LeafNode_links(self):
        node = LeafNode("a", "Click me!", {"href": "https://example.com"})
        self.assertEqual(node.to_html(), '<a href="https://example.com">Click me!</a>')

    def test_leafnode_multiple_attributes(self):
        node = LeafNode("img", None, {"src": "cat.png", "alt": "A cat"})
        # What should this return or raise?

    def test_leafnode_raises(self):
        with self.assertRaises(ValueError):
            LeafNode("p").to_html()


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_no_tag(self):
        """Test that ValueError is raised when tag is None"""
        with self.assertRaises(ValueError):
            parent_node = ParentNode(None, [LeafNode("span", "child")])
            parent_node.to_html()
    
    def test_to_html_no_children(self):
        """Test that ValueError is raised when children is None"""
        with self.assertRaises(ValueError):
            parent_node = ParentNode("div", None)
            parent_node.to_html()
    
    def test_to_html_empty_children_list(self):
        """Test with an empty children list"""
        parent_node = ParentNode("div", [])
        self.assertEqual(parent_node.to_html(), "<div></div>")


if __name__ == "__main__":
    unittest.main()

