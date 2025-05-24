from src.textnode import TextNode, TextType
from src.markdown import extract_markdown_images, extract_markdown_links

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_list = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_list.append(node)
            continue

        text = node.text
        parts = text.split(delimiter)

        if len(parts) % 2 == 0:
            raise Exception(f"Closing delimiter '{delimiter}' found without matching opening delimiter")

        if len(parts) == 1:
            new_list.append(node)
            continue

        for i in range(len(parts)):
            if i % 2 == 0: # Regular text
                if parts[i]:
                    new_list.append(TextNode(parts[i], TextType.TEXT))
            else:
                if i + 1 < len(parts):
                        new_list.append(TextNode(parts[i], text_type))
                else:
                    raise Exception(f"No closing delimiter '{delimiter}' found")



    return new_list



def split_nodes_image(old_nodes):
    new_nodes = []

    for node in old_nodes:

        if node.text_type == TextType.TEXT:
            text_to_process = node.text
            images = extract_markdown_images(text_to_process)
            while images:
                alt, url = images[0]
                markdown = f"![{alt}]({url})"
                sections = text_to_process.split(markdown, 1)
                
                if sections[0]:
                    new_nodes.append(TextNode(sections[0], TextType.TEXT))
                new_nodes.append(TextNode(alt, TextType.IMAGE, url))
                text_to_process = sections[1]
                images = extract_markdown_images(text_to_process)
                
            if text_to_process:
                new_nodes.append(TextNode(text_to_process, TextType.TEXT))

        else:
            new_nodes.append(node)

        
        
    return new_nodes




def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:

        if node.text_type == TextType.TEXT:
            text_to_process = node.text
            links = extract_markdown_links(text_to_process)
            while links:
                link_text, url = links[0]
                markdown = f"[{link_text}]({url})"
                sections = text_to_process.split(markdown, 1)
                
                if sections[0]:
                    new_nodes.append(TextNode(sections[0], TextType.TEXT))
                new_nodes.append(TextNode(link_text, TextType.LINK, url))
                text_to_process = sections[1]
                links = extract_markdown_links(text_to_process)
                
            if text_to_process:
                new_nodes.append(TextNode(text_to_process, TextType.TEXT))

        else:
            new_nodes.append(node)

        
        
    return new_nodes




def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)  
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes


