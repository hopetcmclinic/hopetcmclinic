import os
import shutil
import subprocess
import sys
from builder import SimpleSiteCMS, run_tailwind

# Configuration
DIST_DIR = '../dist'
REPO_URL = 'git@github.com:hopetcmclinic/hopetcmclinic.git'
BRANCH = 'gh-pages'

def run_command(command, cwd=None, exit_on_error=True):
    """Run a shell command and handle errors."""
    try:
        print(f"Running: {' '.join(command)}")
        subprocess.run(command, check=True, cwd=cwd)
    except subprocess.CalledProcessError as e:
        print(f"Error: Command '{' '.join(command)}' failed.")
        if exit_on_error:
            sys.exit(1)

def build_site():
    """Build the website using the existing build system."""
    print("Building website...")
    try:
        run_tailwind()
        cms = SimpleSiteCMS()
        cms.publish()
        print("Build completed successfully.")
    except Exception as e:
        print(f"Build failed: {e}")
        sys.exit(1)

def deploy():
    """Deploy the contents of dist/ to the gh-pages branch."""
    
    # 1. Build the site to ensure fresh content
    build_site()

    # Absolute path to dist directory
    dist_path = os.path.abspath(DIST_DIR)
    
    if not os.path.exists(dist_path):
        print(f"Error: Dist directory '{dist_path}' does not exist.")
        sys.exit(1)

    # 2. Prepare the dist directory as a git repo
    print(f"Deploying from {dist_path}...")
    
    # Initialize a new git repo inside dist
    # We remove any existing .git directory to start fresh every time
    git_dir = os.path.join(dist_path, '.git')
    if os.path.exists(git_dir):
        shutil.rmtree(git_dir)
        
    run_command(['git', 'init'], cwd=dist_path)
    run_command(['git', 'add', '-A'], cwd=dist_path)
    run_command(['git', 'commit', '-m', 'Deploy to GitHub Pages'], cwd=dist_path)
    
    # 3. Force push to the gh-pages branch
    print(f"Pushing to {BRANCH} branch...")
    run_command(['git', 'push', '-f', REPO_URL, f'master:{BRANCH}'], cwd=dist_path)
    
    print("Deployment complete!")

if __name__ == "__main__":
    deploy()
