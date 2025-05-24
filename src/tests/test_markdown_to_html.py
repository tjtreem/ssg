import unittest
from src.markdown_to_html import markdown_to_html_node
from src.htmlnode import to_html



class TestMarkdownToHtml(unittest.TestCase):


    def test_paragraph(self):
        md = """

This is a **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
    

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html, "<div><p>This is a <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )



    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html, "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )   



    def test_headings(self):
        md = """
# Heading 1

## Heading 2

### Heading 3
"""
    
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading 1</h1><h2>Heading 2</h2><h3>Heading 3</h3></div>",
        )


    def test_blockquote(self):
        md = """
> This is a blockquote
> with multiple lines
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote with multiple lines</blockquote></div>",
        )



    def test_unordered_list(self):
        md = """
* Item 1
* Item 2
* Item 3
"""
    
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul></div>",
        )


    def test_ordered_list(self):
        md = """
1. First item
2. Second item
3. Third item
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>First item</li><li>Second item</li><li>Third item</li></ol></div>",
        )





