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
    url = "https://github.com/tailwindlabs/tailwindcss/releases/latest/download/tailwindcss-macos-arm64" if is_mac() \
        else "https://github.com/tailwindlabs/tailwindcss/releases/latest/download/tailwindcss-linux-x64"    
    urllib.request.urlretrieve(url, "tailwindcss")
    os.chmod("tailwindcss", 0o755)

# Compile and minify your CSS for production
subprocess.run(['./tailwindcss -i ./templates/styles.css -o ../styles.css --minify'], shell=True)


# Define the template directory and set up the environment
file_loader = FileSystemLoader('templates')
env = Environment(loader=file_loader)

class Page:
    def __init__(self):
        self.title = ''


class Article:
    def __init__(self, name='', title='', publish_date='', image='', abstract='', page_title=''):
        self.name = name
        self.title = title
        self.publish_date = publish_date
        self.image = image
        self.abstract = abstract
        self.page_title = page_title


def publishPage(name, title, description, articles):
    template = env.get_template('main.html')
    data = {        
        'name': name,
        'title': title,
        'description': description,
        'articles': articles
    }
    output = template.render(data)

    # Write the rendered HTML to a file
    filename = f'../{name}.html'
    with open(filename, 'w') as f:
        f.write(output)


def publishBlog(article: Article):
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


pages = [
    [
        'index',
        'Hope TCM Clinic - Acupuncture, Herbs, Cupping, Gua Sha & Traditional Chinese Medicine in New Westminster, ICBC',
        "Welcome to Hope Traditional Chinese Medicine Clinic, nestled in the heart of New Westminster, where ancient healing meets modern wellness. Led by the seasoned acupuncturist Eva (RAc, Dr. of TCM), our clinic offers a diverse array of traditional Chinese medicine services including acupuncture, cupping, moxibustion, guasha, and herbal medicine."
    ],
    [
        'therapists',
        'Eva Fang Yuan - Acupuncturist in New Westminster | Hope TCM Clinic',
        "Eva Fang Yuan, a CTCMA-registered Doctor of Traditional Chinese Medicine, graduated from Tzu Chi International College in Vancouver. Specializing in digestive issues, emotional disturbances, and women’s health, she offers acupuncture, FSN, herbal remedies, cupping, auricular acupuncture, moxibustion, and gua sha. Advocating for natural wellness, she integrates Taoist philosophy into her practice."
    ],
    [
        'treatments', 
        'Acupuncture, Herbs, Cupping, Gua Sha & Traditional Chinese Medicine in New Westminster | Hope TCM Clinic', 
        "We offer wide range of traditional chinese medicine treatmeats, including acupuncture, cupping, moxibustion, guasha, and herbal medicine."],
    [
        'blog', 'Blog - Acupuncture, Health Tips | Hope TCM Clinic', ""],
    [
        'contact', 'Contact Hope TCM Clinic in New Westminster - Pain Relief & Health', ""]
]

articles = [
    Article(
        name='cupping',
        page_title='Exploring the Timeless Therapy of Cupping in Traditional Chinese Medicine | Hope TCM Clinic',
        title="Exploring the Timeless Therapy of Cupping in Traditional Chinese Medicine",
        publish_date='March 10, 2024',
        image='cupping.jpg',
        abstract="In the intricate tapestry of Traditional Chinese Medicine (TCM), cupping stands as a practice steeped in centuries of history and revered for its profound therapeutic benefits. Originating in ancient China and transcending cultural boundaries, cupping has emerged as a timeless healing modality that continues to captivate and intrigue both practitioners and enthusiasts worldwide..."
    ),
    Article(
        name='moxibustion',
        page_title='Exploring the Ancient Art of Moxibustion in Traditional Chinese Medicine | Hope TCM Clinic',
        title="Exploring the Ancient Art of Moxibustion in Traditional Chinese Medicine",
        publish_date='March 10, 2024',
        image='moxibustion.jpg',
        abstract="In the realm of ancient healing practices, Traditional Chinese Medicine (TCM) stands as a testament to the enduring wisdom of millennia-old traditions. Among its many modalities, moxibustion holds a significant place, offering a fascinating insight into the intricate interplay between mind, body, and energy flow..."
    ),
    Article(
        name='acupuncture',
        page_title='Exploring the Healing Art of Acupuncture: A Comprehensive Guide to Traditional Therapy | Hope TCM Clinic',
        title="Exploring the Healing Art of Acupuncture: A Comprehensive Guide to Traditional Therapy",
        publish_date='March 2, 2024',
        image='acupuncture.jpeg',
        abstract="Acupuncture, an ancient healing practice rooted in Traditional Chinese Medicine (TCM), has garnered widespread recognition and acclaim for its effectiveness in treating a myriad of health conditions. With a history spanning over 2,000 years, acupuncture remains a cornerstone of holistic healthcare, offering a safe, natural, and non-invasive approach to healing. In this article, we delve into the fascinating world of acupuncture, exploring its origins, principles, techniques, and potential benefits.."
    ),
    Article(
        name='tcm',
        page_title='Exploring the Essence of Traditional Chinese Medicine: An Introduction to Ancient Healing Wisdom | Hope TCM Clinic',
        title="Exploring the Essence of Traditional Chinese Medicine: An Introduction to Ancient Healing Wisdom",
        publish_date='March 2, 2024', 
        image='tcm.jpg',
        abstract="In the realm of holistic wellness and alternative therapies, Traditional Chinese Medicine (TCM) stands as a beacon of ancient wisdom, offering profound insights into the interconnectedness of mind, body, and spirit. With roots dating back thousands of years, TCM is a comprehensive system of healthcare that has evolved through centuries of observation, experimentation, and refinement."
    ),
]

# Generate root pages
for page in pages:
    name, title, description = page
    publishPage(name, title, description, articles)

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

