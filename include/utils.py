import os

def ensure_datasets_directory():
    os.makedirs("datasets", exist_ok=True)