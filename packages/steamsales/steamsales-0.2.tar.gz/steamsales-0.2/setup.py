# Import
import setuptools

# README + CHANGES
with open("README.md", "r", encoding="utf-8") as a:
    long_description = a.read()

with open("CHANGES.md", "r", encoding="utf-8") as b:
    changes = b.read()

# Setup
setuptools.setup(
    name="steamsales",
    version="0.2",
    author="zédyN",
    author_email="zedyn@protonmail.com",
    description="Wrapper for PrepareYourWallet",
    long_description=long_description + changes,
    long_description_content_type="text/markdown",
    url="https://github.com/zedyn/steamsales",
    project_urls={
        "Bug Tracker": "https://github.com/zedyn/steamsales/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=['requests', 'lxml', 'bs4']
)