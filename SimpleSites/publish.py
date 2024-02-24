from jinja2 import Environment, FileSystemLoader
from lxml import etree
from datetime import datetime

# Define the template directory and set up the environment
file_loader = FileSystemLoader('templates')
env = Environment(loader=file_loader)

class Page:
    def __init__(self):
        self.title = ''


def publishPage(name, title):
    template = env.get_template('main.html')
    data = {        
        'name': name,
        'title': title
    }
    output = template.render(data)

    # Write the rendered HTML to a file
    filename = f'../{name}.html'
    with open(filename, 'w') as f:
        f.write(output)



pages = [
    ['index', 'Hope TCM Clinic - Acupuncture, Herbs, Cupping, Gua Sha & Traditional Chinese Medicine in New Westminster'],
    ['therapists', 'Eva Fang Yuan - Acupuncturist in New Westminster | Hope TCM Clinic'],
    ['treatments', 'Acupuncture, Herbs, Cupping, Gua Sha & Traditional Chinese Medicine in New Westminster | Hope TCM Clinic'],
    ['blog', 'Blog - Acupuncture, Health Tips | Hope TCM Clinic'],
    ['contact', 'Contact Hope TCM Clinic in New Westminster - Pain Relief & Health']
]

for page in pages:
    name, title = page
    publishPage(name, title)


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

