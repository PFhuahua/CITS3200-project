import subprocess
import sys
import os

def pip_install_requirements():
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

def playwright_install():
    subprocess.check_call([sys.executable, "-m", "playwright", "install"])

def main():
    print("Installing Python dependencies from requirements.txt...")
    pip_install_requirements()
    print("Installing Playwright browsers...")
    playwright_install()
    print("All dependencies installed successfully.")

if __name__ == "__main__":
    main()