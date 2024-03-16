import json
from jinja2 import Environment, FileSystemLoader
from lxml import etree
from datetime import datetime
import os
import sys
import urllib.request
import subprocess

def is_mac():
    return sys.platform.startswith('darwin')

# Make sure tailwindcss tool exists
if not os.path.exists("tailwindcss"):
    # If file doesn't exist, download it
    print("Downloading tailwindcss ... ")
    url = "https://github.com/tailwindlabs/tailwindcss/releases/latest/download/tailwindcss-macos-x64" if is_mac() \
        else "https://github.com/tailwindlabs/tailwindcss/releases/latest/download/tailwindcss-linux-x64"    
    urllib.request.urlretrieve(url, "tailwindcss")
    os.chmod("tailwindcss", 0o755)

# Compile and minify your CSS for production
subprocess.run(['./tailwindcss -i ./templates/styles.css -o ../styles.css --minify'], shell=True)


# Define the template directory and set up the environment
file_loader = FileSystemLoader('templates')
env = Environment(loader=file_loader)

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


def publishPage(page: Page, articles):
    template = env.get_template('main.html')

    name = page.name
    data = {        
        'name': page.name,
        'title': page.title,
        'description': page.description,
        'articles': articles
    }
    output = template.render(data)

    # Write the rendered HTML to a file
    filename = f'../{name}.html'
    with open(filename, 'w') as f:
        f.write(output)


def publishBlog(article):
    template = env.get_template('main.html')
    data = {        
        'name': "article",
        "article": article,
        'title': article.page_title,
        'description': article.abstract
    }
    output = template.render(data)

    # Write the rendered HTML to a file
    filename = f'../blogs/{article.name}.html'
    with open(filename, 'w') as f:
        f.write(output)


with open('./data/pages.json', 'r') as f:
    pages = [Page(**p) for p in json.load(f)]

with open('./data/articles.json', 'r') as f:
    articles = [Article(**a) for a in json.load(f)]

# Generate root pages
for page in pages:    
    publishPage(page, articles)

# Gnerate blog articles
for article in articles:
    publishBlog(article)


# Generate sitemap
def generate_sitemap(urls):
    # Define the root element
    urlset = etree.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")

    # Iterate over URLs to add them to the sitemap
    for url in urls:
        url_element = etree.SubElement(urlset, "url")
        loc = etree.SubElement(url_element, "loc")
        loc.text = url
        lastmod = etree.SubElement(url_element, "lastmod")
        lastmod.text = datetime.now().strftime('%Y-%m-%d')

    # Return the formatted XML string
    return etree.tostring(urlset, pretty_print=True, xml_declaration=True, encoding="UTF-8")


def save_sitemap_to_file(sitemap_content, file_path):
    with open(file_path, "wb") as file:
        file.write(sitemap_content)

urls = [
    "https://www.hopetcmclinic.ca/",
    "https://www.hopetcmclinic.ca/therapists.html",
    "https://www.hopetcmclinic.ca/index.html",
    "https://www.hopetcmclinic.ca/treatments.html",
    "https://www.hopetcmclinic.ca/blog.html",
    "https://www.hopetcmclinic.ca/contact.html",
    "https://www.hopetcmclinic.ca/blogs/tcm.html",
    "https://www.hopetcmclinic.ca/blogs/acupuncture.html",
    "https://www.hopetcmclinic.ca/blogs/cupping.html",
    "https://www.hopetcmclinic.ca/blogs/moxibustion.html",
]
sitemap_content = generate_sitemap(urls)
save_sitemap_to_file(sitemap_content, "../sitemap.xml")

