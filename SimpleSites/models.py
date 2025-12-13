from dataclasses import dataclass

@dataclass
class Page:
    name: str=""
    title: str=""
    description: str=""
    template: str=""
    content: str=""
    meta: dict = None


@dataclass
class Article:
    name: str=""
    title: str=""
    publish_date: str=""
    image: str=""
    abstract: str=""
    page_title: str=""
    content: str=""


@dataclass
class SitemapEntry:
    filename: str = ''
    hash: str = ''
    lastmod: str = ''
    touched: bool = False
    
    @staticmethod
    def serialize(entry):
        return {'filename': entry.filename, 'hash': entry.hash, 'lastmod': entry.lastmod}
