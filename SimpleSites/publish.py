import json
from jinja2 import Environment, FileSystemLoader
from lxml import etree
from datetime import datetime
import os
import sys
import urllib.request
import subprocess
import hashlib


def run_tailwind():
    # Make sure tailwindcss tool exists
    if not os.path.exists("tailwindcss"):
        # If file doesn't exist, download it
        print("Downloading tailwindcss ... ")
        is_mac = sys.platform.startswith('darwin')
        url = "https://github.com/tailwindlabs/tailwindcss/releases/latest/download/tailwindcss-macos-x64" if is_mac \
            else "https://github.com/tailwindlabs/tailwindcss/releases/latest/download/tailwindcss-linux-x64"    
        urllib.request.urlretrieve(url, "tailwindcss")
        os.chmod("tailwindcss", 0o755)

    # Compile and minify your CSS for production
    subprocess.run(['./tailwindcss -i ./templates/styles.css -o ../styles.css --minify'], shell=True)


class Page:
    def __init__(self, name='', title='', description=''):
        self.name = name
        self.title = title
        self.description = description


class Article:
    def __init__(self, name='', title='', publish_date='', image='', abstract='', page_title=''):
        self.name = name
        self.title = title
        self.publish_date = publish_date
        self.image = image
        self.abstract = abstract
        self.page_title = page_title


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
    SITEMAP_JSON = './sitemap.json'

    def __init__(self) -> None:        
        file_loader = FileSystemLoader('templates')
        self.env = Environment(loader=file_loader)
        self.sitemap = {}
        self.root_url = 'https://www.hopetcmclinic.ca'
        self.output_path = '../'

    def publish(self) -> None:
        self.sitemap = {}
        if os.path.isfile(self.SITEMAP_JSON):
            with open(self.SITEMAP_JSON, 'r') as f:
                self.sitemap = {item.filename: item for item in [SitemapEntry(**a) for a in json.load(f)]}

        with open('./data/pages.json', 'r') as f:
            pages = [Page(**p) for p in json.load(f)]

        with open('./data/articles.json', 'r') as f:
            articles = [Article(**a) for a in json.load(f)]

        for page in pages:
            self.publish_page(page, articles)
            self.publish_cn_page(page, articles)

        for article in articles:
            self.publish_article(article)
            self.publish_cn_article(article)

        self.generate_sitemap("../sitemap.xml")

    def publish_page(self, page: Page, articles: list[Article]) -> None:        
        template = self.env.get_template('en/main.html')
        data = {        
            'name': page.name,
            'title': page.title,
            'description': page.description,
            'content_template': f"en/pages/{page.name}.html",
            'articles': articles
        }
        html = template.render(data)
        self.write_html(html, f'{page.name}.html')


    def publish_article(self, article: Article):
        template = self.env.get_template('en/main.html')
        data = {        
            'name': "article",
            'content_template': f"en/article.html",
            "article": article,
            'title': article.page_title,
            'description': article.abstract
        }
        html = template.render(data)
        self.write_html(html, f'blogs/{article.name}.html')


    def publish_cn_page(self, page: Page, articles: list[Article]) -> None:
        template = self.env.get_template('cn/main.html')
        data = {        
            'name': page.name,
            'title': page.title,
            'description': page.description,
            'content_template': f"cn/pages/{page.name}.html",
            'articles': articles
        }
        html = template.render(data)
        self.write_html(html, f'cn/{page.name}.html')


    def publish_cn_article(self, article: Article):
        template = self.env.get_template('en/main.html')
        data = {        
            'name': "article",
            'content_template': f"en/article.html",
            "article": article,
            'title': article.page_title,
            'description': article.abstract
        }
        html = template.render(data)
        self.write_html(html, f'cn/blogs/{article.name}.html')


    def write_html(self, html: str, filename: str) -> None:
        with open(f'{self.output_path}{filename}', 'w') as f:
            f.write(html)
        
        # Generate the SHA-256 hash
        input_bytes = html.encode('utf-8')
        hash = hashlib.sha256(input_bytes).hexdigest()

        if filename not in self.sitemap:
            self.sitemap[filename] = SitemapEntry(filename)
        sitemap_entry = self.sitemap[filename]
        if hash != sitemap_entry.hash:
            sitemap_entry.hash = hashlib.sha256(input_bytes).hexdigest()
            sitemap_entry.lastmod = datetime.now().strftime('%Y-%m-%d')
        sitemap_entry.touched = True


    # Generate sitemap
    def generate_sitemap(self, output_filename: str):        
        # Define the root element
        urlset = etree.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")

        tourched_sitemap_entries = [entry for entry in self.sitemap.values() if entry.touched]
        for entry in tourched_sitemap_entries:            
            url_element = etree.SubElement(urlset, "url")
            loc = etree.SubElement(url_element, "loc")
            loc.text = f'{self.root_url}/{entry.filename}'
            lastmod = etree.SubElement(url_element, "lastmod")
            lastmod.text = entry.lastmod        
        sitemap_content = etree.tostring(urlset, pretty_print=True, xml_declaration=True, encoding="UTF-8")
    
        with open(output_filename, "wb") as file:
            file.write(sitemap_content)

        with open(self.SITEMAP_JSON, 'w') as file:
            json.dump(tourched_sitemap_entries, file, default=SitemapEntry.serialize)


if __name__ == "__main__":
    run_tailwind()

    cms = SimpleSiteCMS()
    cms.publish()
