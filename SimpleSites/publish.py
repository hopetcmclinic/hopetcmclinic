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


from translations import TRANSLATIONS

class Config:
    ROOT_URL = 'https://www.hopetcmclinic.ca'
    OUTPUT_PATH = '../dist/'
    SITEMAP_JSON = './sitemap.json'
    SITEMAP_XML = '../dist/sitemap.xml'
    TAILWIND_EXEC = './tailwindcss'
    ARTICLE_DIR = './content/articles/*.md'
    PAGE_DIR_TEMPLATE = './content/pages/{lang}/*.md'
    LANGUAGES = ['en', 'cn']


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

        # Load Articles from Markdown - currently articles are shared/translated via one folder, 
        # but in this design we might want to split them too. For now, assuming articles are just EN or mixed.
        # User only asked to split PAGES for now as per plan.
        # BUT the plan says "Articles" were rendering for both languages from the same object. 
        # We will keep existing logic for articles for now (rendering same content for both EN/CN templates),
        # unless user asked to split articles too. The request was generally about "bilingual support".
        # Let's keep articles global for now to avoid breaking changes, but render them into both sites.
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

        # Render Pages per Language
        for lang in Config.LANGUAGES:
            print(f"Publishing {lang.upper()} sites...")
            
            # Load Pages for this specific language
            page_glob = Config.PAGE_DIR_TEMPLATE.format(lang=lang)
            md_pages = glob.glob(page_glob)
            
            # If no pages found (e.g. if we haven't created cn pages yet), just warn
            if not md_pages:
                print(f"Warning: No content found for language '{lang}' in {page_glob}")
                continue

            current_lang_pages = []
            for md_file in md_pages:
                post = frontmatter.load(md_file)
                filename = os.path.splitext(os.path.basename(md_file))[0]
                
                html_content = markdown.markdown(post.content)
                
                page = Page(
                    name=filename,
                    title=post.get('title', ''),
                    description=post.get('description', ''),
                    template=post.get('template', ''),
                    content=html_content
                )
                current_lang_pages.append(page)

            # Render pages for this language
            for page in current_lang_pages:
                self.render_page(lang, page, articles)

            # Render articles for this language (using shared article data for now)
            # This ensures /cn/blogs/foo.html exists
            for article in articles:
                self.render_article(lang, article)

        self.generate_sitemap(Config.SITEMAP_XML)

    def render_page(self, lang: str, page: Page, articles: list[Article]) -> None:
        template_name = 'main.html' 
        # Check if template exists, if not fallback to en? No, we should assume templates exist.
        try:
            template = self.env.get_template(template_name)
        except:
             print(f"Error: Template {template_name} not found.")
             return

        # Determine content template
        # If page has a specific template defined (e.g. 'pages/blog.html'), use it.
        # Otherwise use default.html
        if page.template and page.template.lower() != 'page':
            # Ensure we look in the language specific dir if the path is relative
            # The frontmatter might say "pages/blog.html".
            # We want to use "{lang}/pages/blog.html".
            # If the user put "pages/blog.html" in frontmatter, we prepend lang.
            
            # Special case: if frontmatter path starts with pages/, we prepend lang/
            # Example: "pages/index.html" -> "en/pages/index.html" or "cn/pages/index.html"
            content_template = f"{lang}/{page.template}"
        else:
            content_template = f"{lang}/pages/default.html"

        filename = f'{page.name}.html' if lang == 'en' else f'{lang}/{page.name}.html'
        
        # Determine link prefix for internal links
        # en -> /therapists.html
        # cn -> /cn/therapists.html
        link_prefix = "" if lang == 'en' else f"/{lang}"

        data = {        
            'lang': lang,
            'name': page.name,
            'title': page.title,
            'description': page.description,
            'content_template': content_template,
            'articles': articles,
            'content': page.content,
            'i18n': TRANSLATIONS[lang],
            'link_prefix': link_prefix
        }
        self.write_html(template.render(data), filename)

    def render_article(self, lang: str, article: Article) -> None:
        template = self.env.get_template('main.html')
        content_template = "en/article.html" # Assuming we share the article detailed view template or use EN for now
        # Ideally we should have cn/article.html too. Let's try to use lang specific if available, else EN.
        
        # Check if we have a lang specific article template
        try:
            self.env.get_template(f"{lang}/article.html")
            content_template = f"{lang}/article.html"
        except:
            content_template = "en/article.html"

        filename = f'blogs/{article.name}.html' if lang == 'en' else f'{lang}/blogs/{article.name}.html'
        
        link_prefix = "" if lang == 'en' else f"/{lang}"

        data = {        
            'lang': lang,
            'name': "article",
            'content_template': content_template,
            "article": article,
            'title': article.page_title,
            'description': article.abstract,
            'i18n': TRANSLATIONS[lang],
            'link_prefix': link_prefix
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
