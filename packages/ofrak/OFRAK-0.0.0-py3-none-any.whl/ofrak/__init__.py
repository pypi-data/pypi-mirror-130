import os

readme_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../README.md"))
with open(readme_path, "r") as f:
    print(f.read().strip().strip("`"))
