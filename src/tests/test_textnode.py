import unittest

from src.textnode import TextNode, TextType



class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_different(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_eq_with_none_url(self):
        node = TextNode("Some text", TextType.BOLD)
        node2 = TextNode("Some text", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq_with_url(self):
        node = TextNode("Some text", TextType.BOLD)
        node2 = TextNode("Some text", TextType.BOLD, "https://example.com")
        self.assertNotEqual(node, node2)





if __name__ == "__main__":
    unittest.main()

