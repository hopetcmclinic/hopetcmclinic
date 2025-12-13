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


class SitemapEntry:
    def __init__(self, filename='', hash='', lastmod=''):
        self.filename = filename
        self.hash = hash
        self.lastmod = lastmod
        self.touched = False
    
    @staticmethod
    def serialize(entry):
        return {'filename': entry.filename, 'hash': entry.hash, 'lastmod': entry.lastmod}
