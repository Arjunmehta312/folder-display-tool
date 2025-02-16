from setuptools import setup, find_packages

setup(
    name="folder-display",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[],
    author="Arjun Mehta",
    author_email="your.email@example.com",
    description="A Python library for displaying and managing folder structures",
    long_description="""
    Folder Structure Display Tool is a Python library for displaying and managing folder structures.
    Features:
    - Display folder structure with proper indentation
    - Export to various formats (Text, HTML, JSON)
    - Exclude specific folders (e.g., node_modules)
    - Include/exclude hidden files
    """,
    long_description_content_type="text/markdown",
    url="https://github.com/Arjunmehta312/folder-display-tool",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
) 