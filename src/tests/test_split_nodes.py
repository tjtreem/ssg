import unittest
from src.textnode import TextNode, TextType
from src.split_nodes import split_nodes_delimiter, split_nodes_image, split_nodes_link, text_to_textnodes

class TestSplitNodes(unittest.TestCase):

    def test_no_delimiters(self):
        node = TextNode("This is just plain text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        assert len(new_nodes) == 1
        assert new_nodes[0].text == "This is just plain text"
        assert new_nodes[0].text_type == TextType.TEXT

    def test_single_delimiter_pair(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        assert len(new_nodes) == 3
        assert new_nodes[0].text == "This is text with a "
        assert new_nodes[0].text_type == TextType.TEXT
        assert new_nodes[1].text == "code block"
        assert new_nodes[1].text_type == TextType.CODE
        assert new_nodes[2].text == " word"
        assert new_nodes[2].text_type == TextType.TEXT

    def test_multiple_delimiters(self):
        node = TextNode("This is `code` and more `code here`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        assert len(new_nodes) == 4
        assert new_nodes[0].text == "This is "
        assert new_nodes[0].text_type == TextType.TEXT
        assert new_nodes[1].text == "code"
        assert new_nodes[1].text_type == TextType.CODE
        assert new_nodes[2].text  == " and more "
        assert new_nodes[2].text_type == TextType.TEXT
        assert new_nodes[3].text == "code here"
        assert new_nodes[3].text_type == TextType.CODE

    def test_different_delimiter(self):
        node = TextNode("This has **bold text** in it", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        assert len(new_nodes) == 3
        assert new_nodes[0].text == "This has "
        assert new_nodes[0].text_type == TextType.TEXT
        assert new_nodes[1].text == "bold text"
        assert new_nodes[1].text_type == TextType.BOLD
        assert new_nodes[2].text == " in it"
        assert new_nodes[2].text_type == TextType.TEXT

    def test_non_text_node(self):
        node = TextNode("This is already bold", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        assert len(new_nodes) == 1
        assert new_nodes[0].text == "This is already bold"
        assert new_nodes[0].text_type == TextType.BOLD

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "Hello, check out [Boot.dev](https://www.boot.dev) for coding!", TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Hello, check out ", TextType.TEXT),
                TextNode("Boot.dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" for coding!", TextType.TEXT),
            ],
            new_nodes,
        )


    def test_text_to_textnodes_plain_text(self):
        text = "This is plain text"
        nodes = text_to_textnodes(text)
        assert len(nodes) == 1
        assert nodes[0].text == "This is plain text"
        assert nodes[0].text_type == TextType.TEXT

    def test_text_to_textnodes_bold_text(self):
        text = "This is **bold** text"
        nodes = text_to_textnodes(text)
        assert len(nodes) == 3
        assert nodes[0].text == "This is "
        assert nodes[0].text_type == TextType.TEXT
        assert nodes[1].text == "bold"
        assert nodes[1].text_type == TextType.BOLD
        assert nodes[2].text == " text"
        assert nodes[2].text_type == TextType.TEXT

    def test_text_to_textnodes_italic_text(self):
        text = "This is _italic_ text"
        nodes = text_to_textnodes(text)
        assert len(nodes) == 3
        assert nodes[0].text == "This is "
        assert nodes[0].text_type == TextType.TEXT
        assert nodes[1].text == "italic"
        assert nodes[1].text_type == TextType.ITALIC
        assert nodes[2].text == " text"
        assert nodes[2].text_type == TextType.TEXT

    def test_text_to_textnodes_code_text(self):
        text = "This is a `code block` example"
        nodes = text_to_textnodes(text)
        assert len(nodes) == 3
        assert nodes[0].text == "This is a "
        assert nodes[0].text_type == TextType.TEXT
        assert nodes[1].text == "code block"
        assert nodes[1].text_type == TextType.CODE
        assert nodes[2].text == " example"
        assert nodes[2].text_type == TextType.TEXT

    def test_text_to_textnodes_image_text(self):
        text = "Here is ![image alt text](https://example.com/image.jpg)"
        nodes = text_to_textnodes(text)
        assert len(nodes) == 2
        assert nodes[0].text == "Here is "
        assert nodes[0].text_type == TextType.TEXT
        assert nodes[1].text == "image alt text"
        assert nodes[1].text_type == TextType.IMAGE
        assert nodes[1].url == "https://example.com/image.jpg"

    def test_text_to_textnodes_link_text(self):
        text = "Check out this [link text](https://example.com)"
        nodes = text_to_textnodes(text)
        assert len(nodes) == 2
        assert nodes[0].text == "Check out this "
        assert nodes[0].text_type == TextType.TEXT
        assert nodes[1].text == "link text"
        assert nodes[1].text_type == TextType.LINK
        assert nodes[1].url == "https://example.com"



















