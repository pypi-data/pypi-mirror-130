from setuptools import setup, find_packages

with open("README.md", "r") as f:
    readme = f.read()

setup(
    name="OFRAK",
    version="0.0.0",
    description=(
        "The Open Firmware Reverse Analysis Konsole (OFRAK) is a modular framework that allows "
        "users to analyze, reverse engineer, and modify binaries."
    ),
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Red Balloon Security",
    url="https://gitlab.com/redballoonsecurity/ofrak",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: Linux",
        "Topic :: Security",
        "Topic :: Software Development :: Embedded Systems",
        "Typing :: Typed",
    ],
    python_requires=">=3.7",
    project_urls={
        "Bug Tracker": "https://gitlab.com/redballoonsecurity/ofrak/-/issues",
    },
)
