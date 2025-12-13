import os
import glob
import frontmatter
import markdown
from datetime import datetime
from markdown.extensions import Extension
from markdown.inlinepatterns import ImageInlineProcessor, IMAGE_LINK_RE
from xml.etree import ElementTree

from site_config import Config
from models import Page, Article

class LazyLoadingImagePattern(ImageInlineProcessor):
    def handleMatch(self, m, data):
        text, index, handled = self.getText(data, m.start(0))
        if not handled:
            return None, None, None

        src, title, index, handled = self.getLink(data, index)
        if not handled:
            return None, None, None

        el = ElementTree.Element('img')
        el.set('src', src)
        el.set('alt', text)
        if title:
            el.set('title', title)
        
        # Add lazy loading!
        el.set('loading', 'lazy')
        
        return el, m.start(0), index

class LazyLoadingImageExtension(Extension):
    def extendMarkdown(self, md):
        md.inlinePatterns.register(LazyLoadingImagePattern(IMAGE_LINK_RE, md), 'image_link', 150)

class ContentLoader:
    def load_pages(self, lang: str) -> list[Page]:
        page_glob = Config.PAGE_DIR_TEMPLATE.format(lang=lang)
        md_pages = glob.glob(page_glob, recursive=True)
        
        if not md_pages:
            print(f"Warning: No content found for language '{lang}' in {page_glob}")
            return []

        pages = []
        base_content_dir = os.path.dirname(Config.PAGE_DIR_TEMPLATE.format(lang=lang).replace('/*.md', '').replace('/**/*.md', ''))
        
        for md_file in md_pages:
            post = frontmatter.load(md_file)
            
            # Calculate relative path from the content root to allow for subdirectories
            rel_path = os.path.relpath(md_file, base_content_dir)
            filename = os.path.splitext(rel_path)[0]
            
            html_content = markdown.markdown(post.content, extensions=[LazyLoadingImageExtension()])
            
            page = Page(
                name=filename,
                title=post.get('title', ''),
                description=post.get('description', ''),
                template=post.get('template', ''),
                content=html_content,
                meta=post.metadata
            )
            pages.append(page)
        return pages

    def load_articles(self, lang: str) -> list[Article]:
        article_glob = Config.ARTICLE_DIR_TEMPLATE.format(lang=lang)
        md_articles = glob.glob(article_glob)
        
        articles = []
        for md_file in md_articles:
            post = frontmatter.load(md_file)
            filename = os.path.splitext(os.path.basename(md_file))[0]
            
            html_content = markdown.markdown(post.content, extensions=[LazyLoadingImageExtension()])
            
            article = Article(
                name=filename,
                title=post.get('title', ''),
                publish_date=str(post.get('date', '')),
                image=post.get('image', ''),
                abstract=post.get('abstract', ''),
                page_title=post.get('page_title', ''),
                content=html_content
            )
            articles.append(article)
        
        # Sort articles
        articles.sort(key=lambda x: self._parse_date(x.publish_date), reverse=True)
        return articles

    def _parse_date(self, date_str):
        for fmt in ('%B %d, %Y', '%Y-%m-%d'):
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                pass
        return datetime.min
