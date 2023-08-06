import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="NekoMimi",
    version="1.0.7",
    author="NekoMimi",
    author_email="mrcreaperwhantsadingdongtobedo@gmail.com",
    description="A handy collection of tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/NekoKitsune/NekoMimi",
    project_urls={
        "Bug Tracker": "https://github.com/NekoKitsune/NekoMimi/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"./": "NekoMimi/"},
    install_requires = ['pyfiglet','requests','BeautifulSoup4'],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
)