import os
import shutil
from textnode import TextNode, TextType
from markdown_utils import markdown_to_html_node, extract_title


def copy_dir_recursive(src: str, dst: str):
    """Recursively copy contents of `src` directory into `dst` directory.

    This removes `dst` first if it exists, then recreates it and copies all
    files and subdirectories. Prints each copied file path.
    """
    if os.path.exists(dst):
        shutil.rmtree(dst)
    os.makedirs(dst, exist_ok=True)

    for name in os.listdir(src):
        src_path = os.path.join(src, name)
        dst_path = os.path.join(dst, name)
        if os.path.isdir(src_path):
            # create directory then recurse
            os.makedirs(dst_path, exist_ok=True)
            copy_dir_recursive(src_path, dst_path)
        else:
            # copy file
            shutil.copy2(src_path, dst_path)
            print(f"copied {src_path} -> {dst_path}")


def main():
    # basepath may be provided as first CLI argument, default '/'
    import sys
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"

    # example usage: copy static -> docs
    copy_dir_recursive("static", "docs")
    # generate pages for all markdown files in content
    try:
        generate_pages_recursive("content", "template.html", "docs", basepath)
    except Exception as e:
        print(f"Error generating pages: {e}")


def generate_page(from_path: str, template_path: str, dest_path: str, basepath: str = "/"):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r", encoding="utf-8") as f:
        md = f.read()

    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()

    node = markdown_to_html_node(md)
    content_html = node.to_html()
    title = extract_title(md)

    page = template.replace("{{ Title }}", title).replace("{{ Content }}", content_html)
    # replace absolute-rooted paths with basepath
    if basepath != "/":
        page = page.replace('href="/', f'href="{basepath}')
        page = page.replace("href='/", f"href='{basepath}")
        page = page.replace('src="/', f'src="{basepath}')
        page = page.replace("src='/", f"src='{basepath}")

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(page)


def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str, basepath: str = "/"):
    """Recursively find markdown files under `dir_path_content` and generate
    HTML pages into `dest_dir_path` mirroring directory structure.
    """
    # read template once
    with open(template_path, 'r', encoding='utf-8') as f:
        template = f.read()

    for root, dirs, files in os.walk(dir_path_content):
        for fname in files:
            if not fname.lower().endswith('.md'):
                continue
            src_path = os.path.join(root, fname)
            # compute relative path from content dir
            rel = os.path.relpath(src_path, dir_path_content)
            # change extension to .html and write into dest_dir_path
            dest_rel = os.path.splitext(rel)[0] + '.html'
            dest_path = os.path.join(dest_dir_path, dest_rel)
            print(f"Generating page from {src_path} to {dest_path} using {template_path}")
            # ensure dest directory exists
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            with open(src_path, 'r', encoding='utf-8') as f:
                md = f.read()
            node = markdown_to_html_node(md)
            content_html = node.to_html()
            title = extract_title(md)
            page = template.replace("{{ Title }}", title).replace("{{ Content }}", content_html)
            # rewrite absolute-rooted URLs to use basepath
            if basepath != "/":
                page = page.replace('href="/', f'href="{basepath}')
                page = page.replace("href='/", f"href='{basepath}")
                page = page.replace('src="/', f'src="{basepath}')
                page = page.replace("src='/", f"src='{basepath}")
            with open(dest_path, 'w', encoding='utf-8') as f:
                f.write(page)


if __name__ == "__main__":
    main()
