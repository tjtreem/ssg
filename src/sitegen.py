import os
from src import markdown
from src import markdown_to_html

# def main(): for debug purposes only

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path) as f:
        markdown_content = f.read()

    with open(template_path) as f:
        template_content = f.read()

    html_node = markdown_to_html.markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()

    try:
        title = markdown.extract_title(markdown_content)
    except Exception as e:
        raise Exception("No title found in the markdown file")

    result = template_content.replace("{{ Title }}", title).replace("{{ Content }}", html_content)

    directory = os.path.dirname(dest_path)

    os.makedirs(directory, exist_ok=True)

    with open(dest_path, "w") as f:
        f.write(result) # 'result' is final HTML string

    # generate_page(
           # "content/index.md",
           # "template.html",
           # "public/index.html"
    #) for debug only

# if __name__ == "__main__":
  #  main() for debug only


