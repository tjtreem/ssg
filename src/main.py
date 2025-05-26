import sys
import shutil
import os
from .sitegen import generate_page


def copy_static_directory(source, destination):
    print(f"Copying from {source} to {destination}") # A helpful log

    if os.path.exists(destination):
        shutil.rmtree(destination)
        
    print(f"Creating destination directory: {destination}")
    os.makedirs(destination) # os.makedirs is useful for creating nested directories

    for item in os.listdir(source):
        source_item_path = os.path.join(source, item)
        destination_item_path = os.path.join(destination, item) # Need a destination path too

        if os.path.isfile(source_item_path):
            print(f"Copying file: {source_item_path} to {destination_item_path}") # Add log here
            shutil.copy(source_item_path, destination_item_path)
        else:
            print(f"Entering directory: {source_item_path}") # Add another log
            copy_static_directory(source_item_path, destination_item_path)

def generate_pages_recursive(source_dir, basepath):
    for item in os.listdir(source_dir):
        source_path = os.path.join(source_dir, item)
        

        if os.path.isfile(source_path):
            if source_path.endswith(".md"):
                destination_path = source_path.replace("content", OUTPUT_DIR_PATH).replace(".md", ".html")
                
                destination_dir = os.path.dirname(destination_path)
                os.makedirs(destination_dir, exist_ok=True)

                generate_page(source_path, "template.html", destination_path, basepath)
                          
        else:
            generate_pages_recursive(source_path, basepath)

STATIC_DIR_PATH = "./static"
# PUBLIC_DIR_PATH = "./public" (for testing purposes)
OUTPUT_DIR_PATH = "./docs"




def main():
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"

    copy_static_directory(STATIC_DIR_PATH, OUTPUT_DIR_PATH)

    generate_page("content/index.md", "template.html", os.path.join(OUTPUT_DIR_PATH, "index.html"), basepath)

    generate_pages_recursive("content", basepath)

if __name__ == "__main__":
    main()






