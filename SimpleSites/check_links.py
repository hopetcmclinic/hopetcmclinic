
import os
import sys
import argparse
from urllib.parse import urlparse, urljoin, unquote
from html.parser import HTMLParser
import concurrent.futures
import urllib.request

class LinkExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for attr, value in attrs:
                if attr == 'href':
                    self.links.append(value)
        elif tag == 'img':
             for attr, value in attrs:
                if attr == 'src':
                    self.links.append(value)
        elif tag == 'link':
             for attr, value in attrs:
                if attr == 'href':
                    self.links.append(value)
        elif tag == 'script':
             for attr, value in attrs:
                if attr == 'src':
                    self.links.append(value)

def get_all_files(root_dir):
    html_files = []
    for dirpath, _, filenames in os.walk(root_dir):
        for f in filenames:
            if f.endswith('.html'):
                html_files.append(os.path.join(dirpath, f))
    return html_files

def check_external_link(url):
    try:
        req = urllib.request.Request(url, method='HEAD')
        # Mimic a browser to avoid some 403s
        req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36')
        with urllib.request.urlopen(req, timeout=5) as response:
            return response.status < 400
    except Exception as e:
        # Retry with GET if HEAD fails (sometimes servers block HEAD)
        try:
             req = urllib.request.Request(url, method='GET')
             req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36')
             with urllib.request.urlopen(req, timeout=5) as response:
                return response.status < 400
        except Exception:
            return False

def validate_internal_link(base_file, link, root_dir):
    # Ignore anchors, mailto, tel
    if link.startswith('mailto:') or link.startswith('tel:') or link.startswith('javascript:'):
        return True
    
    # Strip anchor
    link_path = link.split('#')[0]
    if not link_path: # Just an anchor on same page
        return True

    # Check if absolute path (relative to site root) or relative to file
    if link_path.startswith('/'):
        # Relative to site root
        # Remove leading slash and join with root_dir
        target_path = os.path.join(root_dir, link_path.lstrip('/'))
    else:
        # Relative to current file
        target_path = os.path.join(os.path.dirname(base_file), link_path)

    # Normalize path
    target_path = os.path.abspath(target_path)
    
    # Check existence
    # Try as file
    if os.path.isfile(target_path):
        return True
    
    # Try as directory (implies index.html)
    if os.path.isdir(target_path):
        if os.path.isfile(os.path.join(target_path, 'index.html')):
            return True
            
    return False

def scan_site(dist_dir, check_external=False):
    files = get_all_files(dist_dir)
    print(f"Scanning {len(files)} HTML files in {dist_dir}...")
    
    broken_links = []
    
    # For internal link checking
    internal_check_cache = {}

    external_links_to_check = set()

    for file_path in files:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        parser = LinkExtractor()
        parser.feed(content)
        
        for link in parser.links:
            # Skip empty links
            if not link: 
                continue

            parsed = urlparse(link)
            
            if parsed.scheme in ('http', 'https'):
                if check_external:
                    external_links_to_check.add((file_path, link))
            elif not parsed.scheme:
                # Internal link
                is_valid = validate_internal_link(file_path, link, dist_dir)
                if not is_valid:
                    broken_links.append((file_path, link, "Internal file not found"))
    
    # Check external links concurrently
    if check_external and external_links_to_check:
        print(f"Checking {len(external_links_to_check)} external links...")
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            future_to_link = {executor.submit(check_external_link, link): (fp, link) for fp, link in external_links_to_check}
            for future in concurrent.futures.as_completed(future_to_link):
                fp, link = future_to_link[future]
                try:
                    if not future.result():
                         broken_links.append((fp, link, "External link unreachable"))
                except Exception as e:
                     broken_links.append((fp, link, f"External link error: {str(e)}"))

    return broken_links

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Scan static site for dead links.')
    parser.add_argument('--dist', default='../dist', help='Path to dist directory')
    parser.add_argument('--external', action='store_true', help='Check external links')
    
    args = parser.parse_args()
    
    abs_dist = os.path.abspath(args.dist)
    
    if not os.path.exists(abs_dist):
        print(f"Error: Dist directory not found at {abs_dist}")
        sys.exit(1)
        
    broken = scan_site(abs_dist, args.external)
    
    if broken:
        print(f"\nFound {len(broken)} broken links:")
        for source, link, reason in broken:
            rel_source = os.path.relpath(source, abs_dist)
            print(f"  [{reason}] In '{rel_source}': {link}")
        sys.exit(1)
    else:
        print("\nNo broken links found!")
        sys.exit(0)
