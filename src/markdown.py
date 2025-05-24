import re


def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches



def markdown_to_blocks(markdown):
    # Split by double newlines and clean up each block
    blocks = [block.strip() for block in markdown.split("\n\n") if block.strip()]

    return blocks


def extract_title(markdown):
    lines = markdown.split("\n")

    for line in lines:
        if line.startswith("#") and not line.startswith("##"):
            title = line[1:].strip()
            if title:
                return title

    else:
        raise ValueError("No header found")


