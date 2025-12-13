class Config:
    ROOT_URL = 'https://www.hopetcmclinic.ca'
    OUTPUT_PATH = '../dist/'
    SITEMAP_JSON = './sitemap.json'
    SITEMAP_XML = '../dist/sitemap.xml'
    TAILWIND_EXEC = './tailwindcss'
    ARTICLE_DIR_TEMPLATE = './content/articles/{lang}/*.md'
    PAGE_DIR_TEMPLATE = './content/pages/{lang}/**/*.md'
    LANGUAGES = ['en', 'cn']
