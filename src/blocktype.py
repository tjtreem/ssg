import re
from enum import Enum


class BlockType(Enum):
    paragraph = "paragraph"
    heading = "heading"
    code = "code"
    quote = "quote"
    unordered_list = "unordered_list"
    ordered_list = "ordered_list"


def block_to_block_type(markdown):
    lines = markdown.splitlines()

    if not lines:
        return BlockType.paragraph

    elif re.match(r"^#{1,6} ", lines[0]):
        return BlockType.heading

    elif lines[0] == "```" and lines[-1] == "```":
        return BlockType.code

    elif all(line.startswith(">") for line in lines):
        return BlockType.quote

    elif all(line.startswith("- ") or line.startswith("* ") or line.startswith("+ ") for line in lines):
        return BlockType.unordered_list

    elif all(line.startswith(f"{index + 1}. ") for index, line in enumerate(lines)):
        return BlockType.ordered_list

    else:
        return BlockType.paragraph


