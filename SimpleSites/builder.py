import json
import os
import hashlib
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from lxml import etree

from site_config import Config
from models import Page, Article, SitemapEntry
from translations import TRANSLATIONS
from asset_manager import AssetManager
from content_loader import ContentLoader

def run_tailwind():
   AssetManager().run_tailwind()

class SimpleSiteCMS():
    def __init__(self) -> None:        
        file_loader = FileSystemLoader('templates')
        self.env = Environment(loader=file_loader)
        self.sitemap = {}
        self.assets = AssetManager()
        self.loader = ContentLoader()

    def publish(self) -> None:
        self.sitemap = {}
        if os.path.isfile(Config.SITEMAP_JSON):
            with open(Config.SITEMAP_JSON, 'r') as f:
                self.sitemap = {item.filename: item for item in [SitemapEntry(**a) for a in json.load(f)]}
        
        # 1. Manage Assets
        self.assets.copy_assets()
        self.assets.process_hashed_assets()

        # 2. Build Pages for each Language
        for lang in Config.LANGUAGES:
            print(f"Publishing {lang.upper()} sites...")
            
            pages = self.loader.load_pages(lang)
            articles = self.loader.load_articles(lang)

            if not pages:
                continue

            # Render pages
            for page in pages:
                self.render_page(lang, page, articles)

            # Render articles
            for article in articles:
                self.render_article(lang, article)

        # 3. Finalize
        self.generate_sitemap(Config.SITEMAP_XML)
        self.generate_robots_txt()

    def render_page(self, lang: str, page: Page, articles: list[Article]):
        template = self.env.get_template('main.html')
        
        # Determine content template (moved logic inside for now, could be in model)
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
            
        # Pseudo-article support
        page_as_article = None
        if content_template == "pages/article.html" or content_template.endswith("/article.html"):
            page_as_article = Article(
                title=page.title,
                content=page.content,
            )

        html = template.render(
            lang=lang, 
            link_prefix=link_prefix,
            i18n=TRANSLATIONS[lang], 
            page=page.meta, 
            articles=articles,
            article=page_as_article, 
            title=page.title, 
            description=page.description,
            name=page.name,
            content_template=content_template,
            canonical_url=canonical_url,
            alternates=alternates,
            root_url=Config.ROOT_URL,
            keywords=page.keywords,
            structured_data=self._generate_structured_data(lang, page, is_article=False),
            css_file=getattr(self.assets, 'css_file', 'styles.css'),
            js_file=getattr(self.assets, 'js_file', 'script.js'),
            content=page.content
        )
        
        self.write_html(html, output_filename)

    def render_article(self, lang: str, article: Article) -> None:
        template = self.env.get_template('main.html')
        content_template = "pages/article.html"
        
        filename = f'blogs/{article.name}.html' if lang == 'en' else f'{lang}/blogs/{article.name}.html'
        link_prefix = "" if lang == 'en' else f"/{lang}"

        # Calculate alternates
        alternates = []
        for l in Config.LANGUAGES:
            alt_prefix = "" if l == 'en' else f"/{l}"
            alt_url = f"{Config.ROOT_URL}{alt_prefix}/blogs/{article.name}.html"
            alternates.append({'lang': l, 'href': alt_url})

        canonical_url = f"{Config.ROOT_URL}{link_prefix}/blogs/{article.name}.html"

        data = {        
            'lang': lang,
            'name': "article",
            'content_template': content_template,
            "article": article,
            'title': article.page_title, 
            'description': article.abstract, 
            'i18n': TRANSLATIONS[lang],
            'link_prefix': link_prefix,
            'canonical_url': canonical_url,
            'alternates': alternates,
            'root_url': Config.ROOT_URL,
            'keywords': article.keywords,
            'structured_data': self._generate_structured_data(lang, article, is_article=True),
            'css_file': getattr(self.assets, 'css_file', 'styles.css'),
            'js_file': getattr(self.assets, 'js_file', 'script.js')
        }
        self.write_html(template.render(data), filename)

    def write_html(self, html: str, filename: str) -> None:
        file_path = f'{Config.OUTPUT_PATH}{filename}'
        # Ensure directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # Minify HTML
        if Config.MINIFY_HTML:
            try:
                import htmlmin
                html = htmlmin.minify(html, remove_empty_space=True)
            except ImportError:
                print("Warning: htmlmin not installed. Skipping minification.")

        with open(file_path, 'w') as f:
            f.write(html)
        
        # Sitemap hashing logic
        input_bytes = html.encode('utf-8')
        file_hash = hashlib.sha256(input_bytes).hexdigest()

        if filename not in self.sitemap:
            self.sitemap[filename] = SitemapEntry(filename)
        sitemap_entry = self.sitemap[filename]
        if file_hash != sitemap_entry.hash:
            sitemap_entry.hash = file_hash
            sitemap_entry.lastmod = datetime.now().strftime('%Y-%m-%d')
        sitemap_entry.touched = True

    def generate_sitemap(self, output_filename: str):        
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
            json.dump(touched_sitemap_entries, file, default=SitemapEntry.serialize, indent=4)

    def generate_robots_txt(self):
        content = f"User-agent: *\nAllow: /\nSitemap: {Config.ROOT_URL}/sitemap.xml"
        output_file = os.path.join(Config.OUTPUT_PATH, 'robots.txt')
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, 'w') as f:
            f.write(content)

    def _generate_structured_data(self, lang, obj, is_article=False):
        base_url = Config.ROOT_URL
        data = {
            "@context": "https://schema.org",
            "@type": "WebPage",
            "name": obj.title,
            "url": f"{base_url}/{lang}/{obj.name}.html" if lang != 'en' else f"{base_url}/{obj.name}.html"
        }

        # Home Page logic
        if not is_article and obj.name in ['index', 'home']:
             data.update({
              "@type": "MedicalClinic",
              "name": "Hope Traditional Chinese Medicine Clinic",
              "image": f"{base_url}/images/logo.png",
              "logo": f"{base_url}/images/logo.png",
              "@id": base_url,
              "url": base_url,
              "telephone": "+17788711439",
              "priceRange": "$$",
              "address": {
                "@type": "PostalAddress",
                "streetAddress": "235-889 Carnarvon St, Buzzer 235",
                "addressLocality": "New Westminster",
                "addressRegion": "BC",
                "postalCode": "V3M1G2",
                "addressCountry": "CA"
              },
              "geo": {
                "@type": "GeoCoordinates",
                "latitude": 49.201396,
                "longitude": -122.912630
              },
              "hasMap": "https://www.google.com/maps/search/?api=1&query=Hope+Traditional+Chinese+Medicine+Clinic+New+Westminster", 
              "openingHoursSpecification": {
                "@type": "OpeningHoursSpecification",
                "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
                "opens": "09:00",
                "closes": "18:00"
              },
              "contactPoint": {
                "@type": "ContactPoint",
                "telephone": "+1-778-871-1439",
                "contactType": "customer service",
                "areaServed": "CA",
                "availableLanguage": ["en", "zh"]
              }
            })
        
        # Article logic
        elif is_article:
            data.update({
                "@type": "BlogPosting",
                "headline": obj.title,
                "datePublished": obj.publish_date,
                "author": {
                    "@type": "Organization",
                    "name": "Hope TCM Clinic"
                }
            })
            if obj.image:
                # Assuming article images are in /images/blogs/ relative to root if not absolute
                img_url = obj.image
                if not img_url.startswith('http') and not img_url.startswith('/'):
                    img_url = f"/images/blogs/{img_url}"
                
                if not img_url.startswith('http'):
                     img_url = f"{base_url}{img_url}"
                     
                data["image"] = img_url
                
        return json.dumps(data, indent=2)
