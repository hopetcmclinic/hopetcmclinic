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


def publishPage(name, title, description):
    template = env.get_template('main.html')
    data = {        
        'name': name,
        'title': title,
        'description': description
    }
    output = template.render(data)

    # Write the rendered HTML to a file
    filename = f'../{name}.html'
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

for page in pages:
    name, title, description = page
    publishPage(name, title, description)


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
    "https://www.hopetcmclinic.ca/index.html",
    "https://www.hopetcmclinic.ca/treatments.html",
    "https://www.hopetcmclinic.ca/faq.html",
    "https://www.hopetcmclinic.ca/blog.html",
    "https://www.hopetcmclinic.ca/contact.html"
]
sitemap_content = generate_sitemap(urls)
save_sitemap_to_file(sitemap_content, "../sitemap.xml")

