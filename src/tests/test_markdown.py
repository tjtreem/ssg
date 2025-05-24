import unittest
from src.markdown import extract_markdown_images, extract_markdown_links, markdown_to_blocks, extract_title



class TestMarkdown(unittest.TestCase):

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_multiple_markdown_images(self):
        matches = extract_markdown_images(
                "This is text with an ![image1](https://i.imgur.com/first.png) and another ![image2](https://i.imgur.com/second.png)"
        )
        self.assertEqual([
            ("image1", "https://i.imgur.com/first.png"),
            ("image2", "https://i.imgur.com/second.png")
        ], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://example.com)"
        )
        self.assertEqual([("link", "https://example.com")], matches)

    def test_multiple_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link1](https://example.com) and another [link2](https://boot.dev)"
        )
        self.assertEqual([
            ("link1", "https://example.com"),
            ("link2", "https://boot.dev")
        ], matches)


    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""

        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )



    def test_extract_title_from_markdown(self):
        markdown = "# My Awesome Title"
        md = extract_title(markdown)
        self.assertEqual(md, "My Awesome Title")


    def test_extract_multiple_titles_from_markdown(self):
        markdown = ("# My Awesome Title\n# My Favorite Title")
        md = extract_title(markdown)
        self.assertEqual(md, "My Awesome Title")


    def test_extract_not_titles(self):
        markdown = ("## This is not a title")
        with self.assertRaises(ValueError):
            extract_title(markdown)
            
