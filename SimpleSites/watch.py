import os
import sys
import subprocess
from livereload import Server

def run_publish():
    print("Detected change, rebuilding site...")
    # Run the publish script
    # We use subprocess to ensure a clean run each time
    publish_script = os.path.join(os.path.dirname(__file__), "main.py")
    subprocess.run([sys.executable, publish_script])

if __name__ == "__main__":
    # Initialize the server
    server = Server()
    
    # Watch for changes in key directories and files
    # Re-run main.py when changes occur
    server.watch('content/', run_publish)
    server.watch('templates/', run_publish)
    server.watch('assets/', run_publish)
    server.watch('translations.py', run_publish)
    server.watch('site_config.py', run_publish)
    server.watch('models.py', run_publish)
    server.watch('builder.py', run_publish)
    server.watch('asset_manager.py', run_publish)
    server.watch('content_loader.py', run_publish)
    server.watch('main.py', run_publish)
    
    # Also watch tailwind output if you want, but usually watching templates is enough
    # server.watch('templates/styles.css', run_publish) # main.py runs tailwind anyway
    
    # Define the output directory to serve
    current_dir = os.path.dirname(os.path.abspath(__file__))
    dist_dir = os.path.abspath(os.path.join(current_dir, '../dist'))
    
    print(f"Starting Live Reload Server...")
    print(f"Serving directory: {dist_dir}")
    print(f"Open http://localhost:8000 (or http://<your-ip>:8000) in your browser")
    
    # Run the initial build to make sure everything is fresh
    run_publish()
    
    # Start serving
    server.serve(root=dist_dir, port=8000, host='0.0.0.0', open_url_delay=None)
