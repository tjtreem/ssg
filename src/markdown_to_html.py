from src.htmlnode import HTMLNode, ParentNode
from src.textnode import TextNode, TextType
from src.split_nodes import text_to_textnodes
from src.blocktype import BlockType, block_to_block_type
from src.text_node_to_html_node import text_node_to_html_node
from src.markdown import markdown_to_blocks


def text_to_children(text):
    """
    Convert a string of text with inline markdown to a list of HTMLNode objects

    Args:
        text (str): The text containing the inline markdown

    Returns:
        list: A list of HTMLNode objects
    """

    # Step 1: Convert the text to TextNode objects

    text_nodes = text_to_textnodes(text)

    # Step 2: Convert each TextNode to an HTMLNode

    html_nodes = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        html_nodes.append(html_node)

    return html_nodes


def paragraph_to_html_node(block):
    """
    Convert a paragraph block to an HTMLNode

    Args:
        block (str): The paragraph text

    Returns:
        HTMLNode: An HTMLNode representing the paragraph
    """

    text = block.replace("\n", " ")

    # Create children nodes from the paragraph text

    children = text_to_children(text)

    # Create and return a paragraph HTMLNode with the children

    return ParentNode("p", children)


def heading_to_html_node(block):
    """
    Convert a heading block to an HTMLNode

    Args:
        block (str): The heading text including # characters

    Returns:
        HTMLNode: An HTMLNode representing the heading
    """

    # Count the number of # characters to determine heading level

    level = 0
    for char in block:
        if char == '#':
            level += 1
        else:
            break

    # Ensure level is between 1 and 6

    level = min(level, 6)

    # Remove the # characters and any leading/trailing whitespace

    content = block[level:].strip()

    # Create children nodes from the heading text

    children = text_to_children(content)

    # Create and return the appropriate heading HTMLNode

    return ParentNode(f"h{level}", children)


def code_block_to_html_node(block):
    """
    Convert a code block to an HTMLNode

    Args:
        block (str): The code block text including the ``` markers

    Returns:
        HTMLNode: An HTMLNode representing the code block
    """

    # Remove the ``` markers and get the content
    # The content starts after the first line and ends before the last line

    lines = block.split("\n")
    if len(lines) >= 2:
        # Skip the first and last lines which contain ```
        content = "\n".join(lines[1:-1]) + "\n"
    else:
        content = ""

    # Directly create the code node
    text_node = TextNode(content, TextType.TEXT)
    code_node = ParentNode("code", [text_node_to_html_node(text_node)])

    # Wrap the code node in a pre node

    return ParentNode("pre", [code_node])


def quote_to_html_node(block):
    """
    Convert a quote block to an HTMLNode

    Args:
        block (str): The quote text including the > markers

    Returns:
        HTMLNode: an HTMLNode representing the blockquote
    """

    # Remove the > marker and any leading/trailing whitespace from each line

    lines = block.split("\n")
    cleaned_lines = []

    for line in lines:
        if line.startswith(">"):
            # Remove the > and trim whitespace
            
            cleaned_line = line[1:].strip()
            cleaned_lines.append(cleaned_line)
        else:
            # Keep lines without > as they are

            cleaned_lines.append(line.strip())

    # Join the cleaned lines

    content = " ".join(cleaned_lines)

    # Create children nodes from the quote text

    children = text_to_children(content)

    # Create and return a blockquote HTMLNode

    return ParentNode("blockquote", children)


def unordered_list_to_html_node(block):
    """
    Convert an unordered list block to an HTMLNode

    Args:
        block (str): The list text with items marked by -, *, or +

    Returns:
        HTMLNode: An HTMLNode representing the unordered list
    """

    # Split the block into lines

    lines = block.split("\n")

    # Create a list to hold the li nodes

    list_items = []

    # Process each line as a list item
    
    for line in lines:
        # Skip empty lines

        if not line.strip():
            continue

        # Check if the line starts with a list marker

        if line.strip().startswith(("-", "*", "+")):
            # Remove the marker and trim whitespace
            # Find the position right after the marker

            marker_end = line.find(line.strip()[0]) + 1

            # Get the content after the marker

            item_content = line[marker_end:].strip()

            # Create children nodes from the item text

            item_children = text_to_children(item_content)


            # Create an li node for this item

            li_node = ParentNode("li", item_children)

            # Add to our list of items

            list_items.append(li_node)

    # Create and return a ul node containing all the li nodes

    return ParentNode("ul", list_items)


def ordered_list_to_html_node(block):
    """
    Convert an ordered list block to an HTMLNode

    Args:
        block (str): The list text with items marked by numbers (e.g., 1., 2., etc.)

    Returns:
        HTMLNode: An HTMLNode representing the ordered list
    """

    # Split the block into lines

    lines = block.split("\n")

    # Create a list to hold the li nodes

    list_items = []

    # Process each line as a list item

    for line in lines:
        # Skip empty lines

        if not line.strip():
            continue

        # Check if the line starts with a number followed by a period

        stripped_line = line.strip()
        if stripped_line and stripped_line[0].isdigit() and ". " in stripped_line:
            # Find the position after the number and period

            marker_end = stripped_line.find(". ") + 2

            # Get the content after the marker
            
            item_content = stripped_line[marker_end:].strip()

            # Create children nodes from the item text

            item_children = text_to_children(item_content)

            # Create an li node for this item

            li_node = ParentNode("li", item_children)

            # Add to our list of items

            list_items.append(li_node)

    # Create and return an ol node containing all the li nodes

    return ParentNode("ol", list_items)

                                           
def markdown_to_html_node(markdown):
    # For debugging, print("Function called with:", markdown[:30] + "...")
    """
    Convert a markdown string to an HTMLNode

    Args:
        markdown (str): The markdown text to convert

    Returns:
        ParentNode: A ParentNode representing the entire markdown document
    """

    # Create a parent div node to hold all the blocks

    children = []

    # Split the markdown into blocks

    blocks = markdown_to_blocks(markdown)
    # For debugging, print(f"Number of blocks found: {len(blocks)}")
    for i, block in enumerate(blocks):
        # For debugging, print(f"Block {i}: {block[:30]}...")
        pass

    # Process each block

    for block in blocks:
        # Determine the type of block

        block_type = block_to_block_type(block)
        # For debugging, print (f"Block type: {block_type} for: {block[:30]}...")

        # Based on the type, call the appropriate handler function

        if block_type == BlockType.paragraph:
            children.append(paragraph_to_html_node(block))
        elif block_type == BlockType.heading:
            children.append(heading_to_html_node(block))
        elif block_type == BlockType.code:
            children.append(code_block_to_html_node(block))
        elif block_type == BlockType.quote:
            children.append(quote_to_html_node(block))
        elif block_type == BlockType.unordered_list:
            children.append(unordered_list_to_html_node(block))
        elif block_type == BlockType.ordered_list:
            children.append(ordered_list_to_html_node(block))



    # For debugging, print(f"Number of children created: {len(children)}")
    return ParentNode("div", children)




















