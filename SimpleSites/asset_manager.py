import os
import sys
import shutil
import hashlib
import subprocess
import urllib.request
from PIL import Image
from site_config import Config

class AssetManager:
    def __init__(self):
        self.css_file = "styles.css"
        self.js_file = "script.js"

    def run_tailwind(self):
        # Make sure tailwindcss tool exists
        if not os.path.exists("tailwindcss"):
            # If file doesn't exist, download it
            print("Downloading tailwindcss ... ")
            is_mac = sys.platform.startswith('darwin')
            url = "https://github.com/tailwindlabs/tailwindcss/releases/latest/download/tailwindcss-macos-arm64" if is_mac \
                else "https://github.com/tailwindlabs/tailwindcss/releases/latest/download/tailwindcss-linux-x64"
            urllib.request.urlretrieve(url, "tailwindcss")
            os.chmod("tailwindcss", 0o755)
        # else:
        #     print("Tailwindcss already exists: ", os.path.abspath("tailwindcss"))

        # Ensure output directory exists before running tailwind
        os.makedirs(Config.OUTPUT_PATH, exist_ok=True)

        # Compile and minify your CSS for production
        subprocess.run([f'{Config.TAILWIND_EXEC} -i ./templates/styles.css -o ../dist/styles.css --minify'], shell=True)

    def copy_assets(self) -> None:
        print("Copying assets to dist folder...")
        os.makedirs(Config.OUTPUT_PATH, exist_ok=True)
        
        assets = [
            {'src': './assets/images', 'dest': 'images', 'type': 'dir'},
            {'src': './assets/videos', 'dest': 'videos', 'type': 'dir'},
            {'src': './assets/script.js', 'dest': 'script.js', 'type': 'file'},
            {'src': './assets/favicon.ico', 'dest': 'favicon.ico', 'type': 'file'},
            {'src': './assets/CNAME', 'dest': 'CNAME', 'type': 'file'}
        ]

        for asset in assets:
            src = asset['src']
            dest = os.path.join(Config.OUTPUT_PATH, asset['dest'])
            
            if asset['dest'] == 'images' and asset['type'] == 'dir':
                self.process_images_dir(src, dest)
            elif asset['type'] == 'dir':
                if os.path.exists(src):
                    shutil.copytree(src, dest, dirs_exist_ok=True)
            elif asset['type'] == 'file':
                if os.path.exists(src):
                    shutil.copy2(src, dest)

    def process_images_dir(self, src_dir: str, dest_dir: str) -> None:
        if not os.path.exists(src_dir):
            return
        
        # Walk recursively
        for root, dirs, files in os.walk(src_dir):
            rel_path = os.path.relpath(root, src_dir)
            current_dest_dir = os.path.join(dest_dir, rel_path)
            os.makedirs(current_dest_dir, exist_ok=True)
            
            for file in files:
                src_file = os.path.join(root, file)
                dest_file = os.path.join(current_dest_dir, file)
                
                if not self.needs_update(src_file, dest_file):
                    continue

                ext = os.path.splitext(file)[1].lower()
                if ext in ['.jpg', '.jpeg', '.png']:
                    self.optimize_image(src_file, dest_file)
                else:
                    shutil.copy2(src_file, dest_file)

    def needs_update(self, src: str, dest: str) -> bool:
        if not os.path.exists(dest):
            return True
        return os.path.getmtime(src) > os.path.getmtime(dest)

    def optimize_image(self, src: str, dest: str) -> None:
        try:
            with Image.open(src) as img:
                # Resize if > 1920 width
                if img.width > 1920:
                    ratio = 1920 / img.width
                    new_height = int(img.height * ratio)
                    img = img.resize((1920, new_height), Image.Resampling.LANCZOS)
                
                ext = os.path.splitext(dest)[1].lower()
                if ext in ['.jpg', '.jpeg']:
                    if img.mode != 'RGB':
                        img = img.convert('RGB')
                    img.save(dest, 'JPEG', quality=85, optimize=True)
                elif ext in ['.png']:
                    img.save(dest, 'PNG', optimize=True)
                else:
                    img.save(dest)
                print(f"Optimized: {os.path.basename(dest)}")
        except Exception as e:
            print(f"Error optimizing {src}: {e}. Copying instead.")
            shutil.copy2(src, dest)

    def hash_file(self, filepath: str) -> str:
        sha256 = hashlib.sha256()
        with open(filepath, 'rb') as f:
            while True:
                data = f.read(65536)
                if not data:
                    break
                sha256.update(data)
        return sha256.hexdigest()[:8]

    def process_hashed_assets(self) -> None:
        # Process CSS
        css_path = os.path.join(Config.OUTPUT_PATH, 'styles.css')
        if os.path.exists(css_path):
            css_hash = self.hash_file(css_path)
            self.css_file = f"styles.{css_hash}.css"
            new_css_path = os.path.join(Config.OUTPUT_PATH, self.css_file)
            shutil.move(css_path, new_css_path)
        else:
            self.css_file = "styles.css" # Fallback
            print("Warning: styles.css not found")

        # Process JS
        js_path = os.path.join(Config.OUTPUT_PATH, 'script.js')
        if os.path.exists(js_path):
            js_hash = self.hash_file(js_path)
            self.js_file = f"script.{js_hash}.js"
            new_js_path = os.path.join(Config.OUTPUT_PATH, self.js_file)
            shutil.move(js_path, new_js_path)
        else:
            self.js_file = "script.js" # Fallback
