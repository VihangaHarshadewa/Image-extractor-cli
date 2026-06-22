# 🧰 Image-extractor-cli

A simple Python CLI tool that scans your project files, extracts
external image URLs, downloads them locally, and automatically replaces
them with local paths.

It supports: - CSS (`url(...)`) - HTML (`<img src="...">`) -
JavaScript/TypeScript files (basic support)

------------------------------------------------------------------------

## 🚀 Features

-   📥 Downloads images from external URLs
-   🧠 Automatically detects file extensions
-   🔁 Replaces URLs with local asset paths
-   📁 Organizes images inside an `assets/` folder
-   🔢 Clean sequential naming (`image01.jpg`, `image02.png`, ...)
-   🎨 Colored terminal output for better readability
-   ⚡ Works recursively on full projectsa

------------------------------------------------------------------------

## 📦 Installation

Clone the repository:

``` bash
git clone https://github.com/your-username/image-extractor-cli.git
cd image-extractor-cli
```

Install dependencies:

``` bash
pip install requests colorama
```

------------------------------------------------------------------------

## ⚙️ Usage

1.  Place your project files inside a folder (default: `./project`)
2.  Run the script:

``` bash
python image_extractor.py
```

------------------------------------------------------------------------

## 📁 Project Structure

    image-extractor-cli/
    │
    ├── image_extractor.py
    ├── project/            # Your input project files
    │   ├── index.html
    │   ├── styles.css
    │   └── ...
    │
    └── assets/             # Downloaded images (auto-created)
        ├── image01.jpg
        ├── image02.png

------------------------------------------------------------------------

## ✨ Example

### Before

``` html
<img src="https://images.unsplash.com/photo.jpg">
```

### After

``` html
<img src="./assets/image01.jpg">
```

------------------------------------------------------------------------

## 🧠 How it works

1.  Scans all project files
2.  Finds external image URLs using regex
3.  Downloads images using `requests`
4.  Saves them in `/assets`
5.  Rewrites file paths to local images

------------------------------------------------------------------------

## 📌 Configuration

You can change settings inside the script:

``` python
PROJECT_DIR = "./project"
ASSETS_DIR_NAME = "assets"
```

------------------------------------------------------------------------

## ⚠️ Notes

-   Only supports `http/https` image URLs
-   Skips binary files automatically
-   Duplicate URLs are downloaded only once
-   Works best on frontend projects (HTML/CSS/JS)

------------------------------------------------------------------------

## 🔮 Future Improvements

-   CLI arguments support (`--project path`)
-   Parallel downloading (faster performance)
-   BeautifulSoup HTML parsing (instead of regex)
-   Progress bar support
-   Image optimization/compression

------------------------------------------------------------------------

## 📜 License

MIT License --- feel free to use, modify, and share.

------------------------------------------------------------------------

## ⭐ Support

If you like this project, consider giving it a star ⭐ on GitHub.
