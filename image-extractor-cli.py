#!/usr/bin/env python3

import os
import re
import mimetypes
import hashlib
from pathlib import Path
from urllib.parse import urlparse

import requests
from colorama import init, Fore, Style

# Initialize colors
init(autoreset=True)

# ==========================
# CONFIG
# ==========================
PROJECT_DIR = "./"
ASSETS_DIR_NAME = "assets"

FILE_EXTENSIONS = {
    ".css", ".scss", ".sass", ".less",
    ".html", ".htm",
    ".js", ".jsx", ".ts", ".tsx",
}

URL_PATTERN_CSS = re.compile(
    r'url\(\s*[\'"]?(https?://[^\'")]+)[\'"]?\s*\)',
    re.IGNORECASE,
)

IMG_PATTERN_HTML = re.compile(
    r'<img[^>]+src=["\'](https?://[^"\']+)["\']',
    re.IGNORECASE,
)

downloaded = {}
counter = 1


# ==========================
# HELPERS
# ==========================

def log_info(msg):
    print(Fore.CYAN + "[INFO] " + Style.RESET_ALL + msg)

def log_success(msg):
    print(Fore.GREEN + "[OK]   " + Style.RESET_ALL + msg)

def log_warn(msg):
    print(Fore.YELLOW + "[WARN] " + Style.RESET_ALL + msg)

def log_error(msg):
    print(Fore.RED + "[ERR]  " + Style.RESET_ALL + msg)


def get_file_extension(url, response):
    path = urlparse(url).path
    ext = Path(path).suffix

    if ext:
        return ext

    content_type = response.headers.get("Content-Type", "")
    ext = mimetypes.guess_extension(content_type.split(";")[0])

    return ext or ".jpg"


def next_filename(ext):
    global counter
    filename = f"image{counter:02d}{ext}"
    counter += 1
    return filename


def download_image(url, assets_dir):
    if url in downloaded:
        log_info(f"Already downloaded: {url}")
        return downloaded[url]

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        ext = get_file_extension(url, response)
        filename = next_filename(ext)
        filepath = assets_dir / filename

        if not filepath.exists():
            with open(filepath, "wb") as f:
                f.write(response.content)

        downloaded[url] = filename

        log_success(f"Downloaded {filename} <- {url}")
        return filename

    except Exception as e:
        log_error(f"Failed: {url}")
        log_error(str(e))
        return None


def replace_url(url, assets_dir, file_path):
    filename = download_image(url, assets_dir)
    if not filename:
        return url

    rel_path = os.path.relpath(
        assets_dir / filename,
        file_path.parent
    ).replace("\\", "/")

    return rel_path


def process_file(file_path, assets_dir):
    log_info(f"Processing: {file_path}")

    try:
        content = file_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        log_warn(f"Skipped binary file: {file_path}")
        return

    changed = False

    # ==========================
    # CSS url()
    # ==========================
    def css_replace(match):
        nonlocal changed
        url = match.group(1)

        new_url = replace_url(url, assets_dir, file_path)

        if new_url != url:
            changed = True
            return f"url('{new_url}')"

        return match.group(0)

    content = URL_PATTERN_CSS.sub(css_replace, content)

    # ==========================
    # HTML <img src="">
    # ==========================
    def img_replace(match):
        nonlocal changed
        url = match.group(1)

        new_url = replace_url(url, assets_dir, file_path)

        if new_url != url:
            changed = True
            return match.group(0).replace(url, new_url)

        return match.group(0)

    content = IMG_PATTERN_HTML.sub(img_replace, content)

    if changed:
        file_path.write_text(content, encoding="utf-8")
        log_success(f"Updated file: {file_path}")
    else:
        log_info("No changes needed")


def main():
    project_dir = Path(PROJECT_DIR).resolve()
    assets_dir = project_dir / ASSETS_DIR_NAME

    assets_dir.mkdir(exist_ok=True)

    log_info(f"Project: {project_dir}")
    log_info(f"Assets:  {assets_dir}")
    print()

    for root, dirs, files in os.walk(project_dir):
        dirs[:] = [d for d in dirs if d != ASSETS_DIR_NAME]

        for file in files:
            path = Path(root) / file

            if path.suffix.lower() in FILE_EXTENSIONS:
                process_file(path, assets_dir)

    print()
    log_success("ALL DONE 🎉")


if __name__ == "__main__":
    main()