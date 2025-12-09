import json
from jinja2 import Environment, FileSystemLoader
from lxml import etree
from datetime import datetime
from dataclasses import dataclass
import os
import sys
import urllib.request
import subprocess
import hashlib
import glob
import frontmatter
import markdown
import shutil


class Config:
    ROOT_URL = 'https://www.hopetcmclinic.ca'
    OUTPUT_PATH = '../dist/'
    SITEMAP_JSON = './sitemap.json'
    SITEMAP_XML = '../dist/sitemap.xml'
    TAILWIND_EXEC = './tailwindcss'
    ARTICLE_DIR = './content/articles/*.md'
    PAGE_DIR = './content/pages/*.md'


def run_tailwind():
    # Make sure tailwindcss tool exists
    if not os.path.exists("tailwindcss"):
        # If file doesn't exist, download it
        print("Downloading tailwindcss ... ")
        is_mac = sys.platform.startswith('darwin')
        url = "https://github.com/tailwindlabs/tailwindcss/releases/latest/download/tailwindcss-macos-arm64" if is_mac \
            else "https://github.com/tailwindlabs/tailwindcss/releases/latest/download/tailwindcss-linux-x64"
        urllib.request.urlretrieve(url, "tailwindcss")
        os.chmod("tailwindcss", 0o755)
    else:
        print("Tailwindcss already exists: ", os.path.abspath("tailwindcss"))

    # Ensure output directory exists before running tailwind
    os.makedirs(Config.OUTPUT_PATH, exist_ok=True)

    # Compile and minify your CSS for production
    subprocess.run([f'{Config.TAILWIND_EXEC} -i ./templates/styles.css -o {Config.OUTPUT_PATH}styles.css --minify'], shell=True)


@dataclass
class Page:
    name: str=""
    title: str=""
    description: str=""
    template: str=""
    content: str=""


@dataclass
class Article:
    name: str=""
    title: str=""
    publish_date: str=""
    image: str=""
    abstract: str=""
    page_title: str=""
    content: str=""


class SitemapEntry:
    def __init__(self, filename='', hash='', lastmod=''):
        self.filename = filename
        self.hash = hash
        self.lastmod = lastmod
        self.touched = False
    
    @staticmethod
    def serialize(entry):
        return {'filename': entry.filename, 'hash': entry.hash, 'lastmod': entry.lastmod}


class SimpleSiteCMS():
    def __init__(self) -> None:        
        file_loader = FileSystemLoader('templates')
        self.env = Environment(loader=file_loader)
        self.sitemap = {}

    def copy_assets(self) -> None:
        print("Copying assets to dist folder...")
        os.makedirs(Config.OUTPUT_PATH, exist_ok=True)
        
        assets = [
            {'src': './assets/images', 'dest': 'images', 'type': 'dir'},
            {'src': './assets/videos', 'dest': 'videos', 'type': 'dir'},
            {'src': './assets/script.js', 'dest': 'script.js', 'type': 'file'},
            {'src': './assets/favicon.ico', 'dest': 'favicon.ico', 'type': 'file'},
            {'src': './assets/CNAME', 'dest': 'CNAME', 'type': 'file'}
        ]

        for asset in assets:
            src = asset['src']
            dest = os.path.join(Config.OUTPUT_PATH, asset['dest'])
            
            if asset['type'] == 'dir':
                if os.path.exists(src):
                    # shutil.copytree requires destination dir to NOT exist usually, or dirs_exist_ok=True in 3.8+
                    shutil.copytree(src, dest, dirs_exist_ok=True)
            elif asset['type'] == 'file':
                if os.path.exists(src):
                    shutil.copy2(src, dest)

    def publish(self) -> None:
        self.sitemap = {}
        if os.path.isfile(Config.SITEMAP_JSON):
            with open(Config.SITEMAP_JSON, 'r') as f:
                self.sitemap = {item.filename: item for item in [SitemapEntry(**a) for a in json.load(f)]}
        
        # Copy assets first
        self.copy_assets()

        # Load Pages from Markdown
        pages = []
        md_pages = glob.glob(Config.PAGE_DIR)
        for md_file in md_pages:
            post = frontmatter.load(md_file)
            filename = os.path.splitext(os.path.basename(md_file))[0]
            
            # Convert markdown body to HTML if needed
            # For pages with custom template, content might be empty or used inside template
            html_content = markdown.markdown(post.content)
            
            page = Page(
                name=filename,
                title=post.get('title', ''),
                description=post.get('description', ''),
                template=post.get('template', ''),
                content=html_content
            )
            pages.append(page)

        # Load Articles from Markdown
        articles = []
        md_files = glob.glob(Config.ARTICLE_DIR)
        for md_file in md_files:
            post = frontmatter.load(md_file)
            filename = os.path.splitext(os.path.basename(md_file))[0]
            
            # Convert markdown body to HTML
            html_content = markdown.markdown(post.content)
            
            article = Article(
                name=filename,
                title=post.get('title', ''),
                publish_date=str(post.get('date', '')), # Ensure string
                image=post.get('image', ''),
                abstract=post.get('abstract', ''),
                page_title=post.get('page_title', ''),
                content=html_content
            )
            articles.append(article)
        
        # Sort articles by date descending
        # articles.sort(key=lambda x: x.publish_date, reverse=True) 

        for page in pages:
            self.render_page('en', page, articles)
            self.render_page('cn', page, articles)

        for article in articles:
            self.render_article('en', article)
            self.render_article('cn', article)

        self.generate_sitemap(Config.SITEMAP_XML)

    def render_page(self, lang: str, page: Page, articles: list[Article]) -> None:
        template = self.env.get_template(f'{lang}/main.html')
        
        # Determine content template
        # If page has a specific template defined (e.g. 'pages/blog.html'), use it.
        # Otherwise use default.html
        if page.template and page.template.lower() != 'page':
            # Ensure we look in the language specific dir if the path is relative
            # If frontmatter says "pages/blog.html", we prepend {lang}/
            content_template = f"{lang}/{page.template}"
        else:
            content_template = f"{lang}/pages/default.html"

        filename = f'{page.name}.html' if lang == 'en' else f'{lang}/{page.name}.html'
        
        data = {        
            'lang': lang,
            'name': page.name,
            'title': page.title,
            'description': page.description,
            'content_template': content_template,
            'articles': articles,
            'content': page.content 
        }
        self.write_html(template.render(data), filename)

    def render_article(self, lang: str, article: Article) -> None:
        template = self.env.get_template(f'{lang}/main.html')
        content_template = "en/article.html" 
        
        filename = f'blogs/{article.name}.html' if lang == 'en' else f'{lang}/blogs/{article.name}.html'
        
        data = {        
            'lang': lang,
            'name': "article",
            'content_template': content_template,
            "article": article,
            'title': article.page_title,
            'description': article.abstract
        }
        self.write_html(template.render(data), filename)

    def write_html(self, html: str, filename: str) -> None:
        file_path = f'{Config.OUTPUT_PATH}{filename}'
        # Ensure directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, 'w') as f:
            f.write(html)
        
        # Generate the SHA-256 hash
        input_bytes = html.encode('utf-8')
        file_hash = hashlib.sha256(input_bytes).hexdigest()

        if filename not in self.sitemap:
            self.sitemap[filename] = SitemapEntry(filename)
        sitemap_entry = self.sitemap[filename]
        if file_hash != sitemap_entry.hash:
            sitemap_entry.hash = file_hash
            sitemap_entry.lastmod = datetime.now().strftime('%Y-%m-%d')
        sitemap_entry.touched = True

    # Generate sitemap
    def generate_sitemap(self, output_filename: str):        
        # Define the root element
        urlset = etree.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")

        touched_sitemap_entries = [entry for entry in self.sitemap.values() if entry.touched]
        for entry in touched_sitemap_entries:            
            url_element = etree.SubElement(urlset, "url")
            loc = etree.SubElement(url_element, "loc")
            loc.text = f'{Config.ROOT_URL}/{entry.filename}'
            lastmod = etree.SubElement(url_element, "lastmod")
            lastmod.text = entry.lastmod        
        sitemap_content = etree.tostring(urlset, pretty_print=True, xml_declaration=True, encoding="UTF-8")
    
        with open(output_filename, "wb") as file:
            file.write(sitemap_content)

        with open(Config.SITEMAP_JSON, 'w') as file:
            json.dump(touched_sitemap_entries, file, default=SitemapEntry.serialize)


if __name__ == "__main__":
    run_tailwind()

    cms = SimpleSiteCMS()
    cms.publish()
