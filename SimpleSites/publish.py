from jinja2 import Environment, FileSystemLoader

# Define the template directory and set up the environment
file_loader = FileSystemLoader('templates')
env = Environment(loader=file_loader)

class Page:
    pass

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
    ['index', 'Home'],
    ['therapists', 'Therapists'],
    ['treatments', 'Treatments'],
    ['blog', 'Blog'],
    ['contact', 'Contact']    
]

for page in pages:
    name, title = page
    publishPage(name, title)