import unittest
from src.blocktype import BlockType, block_to_block_type


class TestBlockType(unittest.TestCase):
    def test_heading(self):
        self.assertEqual(block_to_block_type("# This is a heading"), BlockType.heading)

    def test_code(self):
        self.assertEqual(
            block_to_block_type("```\nThis is a code block\n```"),
            BlockType.code
        )

    def test_quote(self):
        self.assertEqual(
            block_to_block_type("> This\n>is a\n> multiline\n>quote block"),
            BlockType.quote
        )

    def test_unordered_list(self):
        self.assertEqual(
            block_to_block_type("- This is\n- an unordered\n- multiline list\n- with several items"),
            BlockType.unordered_list
        )

    def test_ordered_list(self):
        self.assertEqual(
            block_to_block_type("1. First item\n2. Second item\n3. Third item\n4. In an ordered list"),
            BlockType.ordered_list
        )

    def test_not_ordered_list(self):
        self.assertEqual(
            block_to_block_type("1. This is\n3. Simply a\n5. Paragraph block type\n6. Since these aren't sequentially numbered"),
            BlockType.paragraph
        )

    def test_paragraph(self):
        self.assertEqual(
            block_to_block_type("This is just a plain line or block of text"),
            BlockType.paragraph
        )







