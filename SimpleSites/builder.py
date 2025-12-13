import json
import os
import sys
import glob
import shutil
import hashlib
import subprocess
import urllib.request
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from lxml import etree
import frontmatter
import markdown
from PIL import Image

from site_config import Config
from models import Page, Article, SitemapEntry
from translations import TRANSLATIONS


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
    # v4 CLI: tailwindcss -i input.css -o output.css --minify
    # No config file needed if configuration is in CSS
    subprocess.run([f'{Config.TAILWIND_EXEC} -i ./templates/styles.css -o ../dist/styles.css --minify'], shell=True)


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
            
            if asset['dest'] == 'images' and asset['type'] == 'dir':
                self.process_images_dir(src, dest)
            elif asset['type'] == 'dir':
                if os.path.exists(src):
                    # shutil.copytree requires destination dir to NOT exist usually, or dirs_exist_ok=True in 3.8+
                    shutil.copytree(src, dest, dirs_exist_ok=True)
            elif asset['type'] == 'file':
                if os.path.exists(src):
                    shutil.copy2(src, dest)

    def process_images_dir(self, src_dir: str, dest_dir: str) -> None:
        if not os.path.exists(src_dir):
            return
        
        # Walk recursively
        for root, dirs, files in os.walk(src_dir):
            rel_path = os.path.relpath(root, src_dir)
            current_dest_dir = os.path.join(dest_dir, rel_path)
            os.makedirs(current_dest_dir, exist_ok=True)
            
            for file in files:
                src_file = os.path.join(root, file)
                dest_file = os.path.join(current_dest_dir, file)
                
                if not self.needs_update(src_file, dest_file):
                    continue

                ext = os.path.splitext(file)[1].lower()
                if ext in ['.jpg', '.jpeg', '.png']:
                    self.optimize_image(src_file, dest_file)
                else:
                    shutil.copy2(src_file, dest_file)

    def needs_update(self, src: str, dest: str) -> bool:
        if not os.path.exists(dest):
            return True
        return os.path.getmtime(src) > os.path.getmtime(dest)

    def optimize_image(self, src: str, dest: str) -> None:
        try:
            with Image.open(src) as img:
                # Resize if > 1920 width
                if img.width > 1920:
                    ratio = 1920 / img.width
                    new_height = int(img.height * ratio)
                    img = img.resize((1920, new_height), Image.Resampling.LANCZOS)
                
                ext = os.path.splitext(dest)[1].lower()
                if ext in ['.jpg', '.jpeg']:
                    if img.mode != 'RGB':
                        img = img.convert('RGB')
                    img.save(dest, 'JPEG', quality=85, optimize=True)
                elif ext in ['.png']:
                    img.save(dest, 'PNG', optimize=True)
                else:
                    img.save(dest)
                print(f"Optimized: {os.path.basename(dest)}")
        except Exception as e:
            print(f"Error optimizing {src}: {e}. Copying instead.")
            shutil.copy2(src, dest)

    def hash_file(self, filepath: str) -> str:
        sha256 = hashlib.sha256()
        with open(filepath, 'rb') as f:
            while True:
                data = f.read(65536)
                if not data:
                    break
                sha256.update(data)
        return sha256.hexdigest()[:8]

    def process_hashed_assets(self) -> None:
        # Process CSS
        css_path = os.path.join(Config.OUTPUT_PATH, 'styles.css')
        if os.path.exists(css_path):
            css_hash = self.hash_file(css_path)
            self.css_file = f"styles.{css_hash}.css"
            new_css_path = os.path.join(Config.OUTPUT_PATH, self.css_file)
            shutil.move(css_path, new_css_path)
        else:
            self.css_file = "styles.css" # Fallback
            print("Warning: styles.css not found")

        # Process JS
        js_path = os.path.join(Config.OUTPUT_PATH, 'script.js')
        if os.path.exists(js_path):
            js_hash = self.hash_file(js_path)
            self.js_file = f"script.{js_hash}.js"
            new_js_path = os.path.join(Config.OUTPUT_PATH, self.js_file)
            shutil.move(js_path, new_js_path)
        else:
            self.js_file = "script.js" # Fallback

    def publish(self) -> None:
        self.sitemap = {}
        if os.path.isfile(Config.SITEMAP_JSON):
            with open(Config.SITEMAP_JSON, 'r') as f:
                self.sitemap = {item.filename: item for item in [SitemapEntry(**a) for a in json.load(f)]}
        
        # Copy assets first
        self.copy_assets()
        
        # Process assets (hash and rename)
        self.process_hashed_assets()



        # Render Pages per Language
        for lang in Config.LANGUAGES:
            print(f"Publishing {lang.upper()} sites...")
            
            # Load Pages for this specific language
            page_glob = Config.PAGE_DIR_TEMPLATE.format(lang=lang)
            # Use recursive glob to find all md files in subdirectories
            md_pages = glob.glob(page_glob, recursive=True)
            
            # If no pages found (e.g. if we haven't created cn pages yet), just warn
            if not md_pages:
                print(f"Warning: No content found for language '{lang}' in {page_glob}")
                
            # Load Articles for this specific language
            articles = []
            article_glob = Config.ARTICLE_DIR_TEMPLATE.format(lang=lang)
            md_articles = glob.glob(article_glob)
            
            for md_file in md_articles:
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
            try:
                # Attempt to parse date with multiple formats if needed, but for now stick to one or string compare? 
                # Original code used '%B %d, %Y' (December 06, 2023). 
                # Chinese dates might be different. Let's try standardizing or being flexible.
                # For now, we'll try the English format, if fail, maybe try ISO?
                # Actually, standardizing input date format to YYYY-MM-DD in frontmatter is best practice.
                # But let's support the legacy format too.
                def parse_date(date_str):
                    for fmt in ('%B %d, %Y', '%Y-%m-%d'):
                        try:
                            return datetime.strptime(date_str, fmt)
                        except ValueError:
                            pass
                    return datetime.min # Fallback
                
                articles.sort(key=lambda x: parse_date(x.publish_date), reverse=True)
            except Exception as e:
                print(f"Warning: Date sorting issue: {e}")

            if not md_pages:
                continue

            current_lang_pages = []
            base_content_dir = os.path.dirname(Config.PAGE_DIR_TEMPLATE.format(lang=lang).replace('/*.md', '').replace('/**/*.md', ''))
            
            for md_file in md_pages:
                post = frontmatter.load(md_file)
                
                # Calculate relative path from the content root to allow for subdirectories
                # e.g. content/pages/en/treatments/acupuncture.md -> treatments/acupuncture
                rel_path = os.path.relpath(md_file, base_content_dir)
                filename = os.path.splitext(rel_path)[0]
                
                html_content = markdown.markdown(post.content)
                
                page = Page(
                    name=filename,
                    title=post.get('title', ''),
                    description=post.get('description', ''),
                    template=post.get('template', ''),
                    content=html_content,
                    meta=post.metadata
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
        self.generate_robots_txt()


    def render_page(self, lang: str, page: Page, articles: list[Article]):
        template = self.env.get_template('main.html')
        
        # Restore content_template determination logic
        if page.template and page.template.lower() != 'page':
            lang_specific_template = f"{lang}/{page.template}"
            if os.path.exists(os.path.join('templates', lang_specific_template)):
                content_template = lang_specific_template
            else:
                content_template = page.template
        else:
            lang_specific_default = f"{lang}/pages/default.html"
            if os.path.exists(os.path.join('templates', lang_specific_default)):
                content_template = lang_specific_default
            else:
                content_template = "pages/default.html"
        
        link_prefix = "" if lang == 'en' else f"/{lang}"
        
        # Calculate alternates
        alternates = []
        for l in Config.LANGUAGES:
            alt_prefix = "" if l == 'en' else f"/{l}"
            alt_url = f"{Config.ROOT_URL}{alt_prefix}/{page.name}.html"
            alternates.append({'lang': l, 'href': alt_url})

        # Calculate canonical
        canonical_url = f"{Config.ROOT_URL}{link_prefix}/{page.name}.html"

        output_filename = f"{page.name}.html"
        if lang != 'en':
            output_filename = f"{lang}/{output_filename}"
            
        


        # If the template is using article.html, we need to pass an 'article' object
        # This is because article.html expects {{ article.title }} and {{ article.content }}
        page_as_article = None
        if content_template == "pages/article.html" or content_template.endswith("/article.html"):
            page_as_article = Article(
                title=page.title,
                content=page.content,
                # Add other fields if needed by article.html
            )

        html = template.render(
            lang=lang, 
            link_prefix=link_prefix,
            i18n=TRANSLATIONS[lang], 
            page=page.meta, 
            articles=articles,
            article=page_as_article, # Pass the pseudo-article
            title=page.title, 
            description=page.description,
            name=page.name,
            content_template=content_template,
            canonical_url=canonical_url,
            alternates=alternates,
            root_url=Config.ROOT_URL,
            css_file=getattr(self, 'css_file', 'styles.css'),
            js_file=getattr(self, 'js_file', 'script.js')
        )
        
        self.write_html(html, output_filename)

    def render_article(self, lang: str, article: Article) -> None:
        template = self.env.get_template('main.html')
        
        # Use unified article template
        content_template = "pages/article.html"

        filename = f'blogs/{article.name}.html' if lang == 'en' else f'{lang}/blogs/{article.name}.html'
        
        link_prefix = "" if lang == 'en' else f"/{lang}"

        # Calculate alternates for articles
        alternates = []
        for l in Config.LANGUAGES:
            alt_prefix = "" if l == 'en' else f"/{l}"
            alt_url = f"{Config.ROOT_URL}{alt_prefix}/blogs/{article.name}.html"
            alternates.append({'lang': l, 'href': alt_url})

        # Calculate canonical for articles
        canonical_url = f"{Config.ROOT_URL}{link_prefix}/blogs/{article.name}.html"

        data = {        
            'lang': lang,
            'name': "article",
            'content_template': content_template,
            "article": article,
            'title': article.page_title, # Assuming page_title is the SEO title for articles
            'description': article.abstract, # Assuming abstract is the SEO description for articles
            'i18n': TRANSLATIONS[lang],
            'link_prefix': link_prefix,
            'canonical_url': canonical_url,
            'canonical_url': canonical_url,
            'alternates': alternates,
            'root_url': Config.ROOT_URL,
            'css_file': getattr(self, 'css_file', 'styles.css'),
            'js_file': getattr(self, 'js_file', 'script.js')
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

    def generate_robots_txt(self):
        content = f"User-agent: *\nAllow: /\nSitemap: {Config.ROOT_URL}/sitemap.xml"
        output_file = os.path.join(Config.OUTPUT_PATH, 'robots.txt')
        # Ensure dir exists (it should, but safety first)
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, 'w') as f:
            f.write(content)
