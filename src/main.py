import sys
from full_converter import extract_title, markdown_to_html_node
import os, shutil

def wipe_directory_content(path):
    with os.scandir(path) as entries:
        for entry in entries:
            if entry.is_dir() and not entry.is_symlink():
                shutil.rmtree(entry.path)
            else:
                os.remove(entry.path)

def copy(source, target): #copies from source directory path to target path
    wipe_directory_content(target)
    changelog = f"{target} content wiped"
    with os.scandir(source) as entries:
        for entry in entries:
            if entry.is_dir() and not entry.is_symlink():
                newdir = f"{target}/{entry.name}"
                os.mkdir(newdir)
                copy(entry, newdir)
                changelog += f"\n directory {entry.name} added to {target}"
            else:
                shutil.copy(entry, target)
                changelog += f"\n file {entry.name} copied to {target}"
    print(changelog)

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, 'r') as file:
        markdown = file.read()
        file.close()
    with open(template_path, 'r') as file:
        template = file.read()
        file.close()
    content = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    if not basepath.endswith("/"):
        basepath += "/"
    html = (
        template
        .replace("{{ Title }}", title)
        .replace("{{ Content }}", content)
        .replace('href="/', f'href="{basepath}')
        .replace('src="/', f'src="{basepath}')
    )
    print(html)
    with open(dest_path, 'w') as f:
        f.write(html)
        f.close()

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    path = os.path.abspath(dir_path_content)
    content = os.listdir(os.path.abspath(path))
    dest_path = os.path.abspath(dest_dir_path)
    for item in content:
        item_path = os.path.join(path, item)
        if os.path.isfile(item_path) and item.endswith(".md"):
            generate_page(item_path, template_path, dest_path + f"/{item[:-3]}.html", basepath)
        elif os.path.isdir(item_path):
            newdir = dest_path + f"/{item}"
            os.makedirs(newdir, exist_ok=True)
            generate_pages_recursive(item_path, template_path, newdir, basepath)


def main():
    basepath = sys.argv[1] if len(sys.argv) >= 2  else "/"
    copy(os.path.abspath("static"), os.path.abspath("docs")) #copies your static files such as images to the docs directory, ready to be used
    generate_pages_recursive(os.path.abspath("content"), os.path.abspath("template.html"), os.path.abspath("docs"), basepath)

if __name__ == "__main__":
    main()