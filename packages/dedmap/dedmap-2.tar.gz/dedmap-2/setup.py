import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dedmap",
    version="2",
    author="Anurag Mondal",
    author_email="7Ragnarok7@pm.me",
    description="A Simple but Powerful cross-platform port scanning & and network automation tool.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/7Ragnarok7/DEDMAP",
    project_urls={
        "Website": "https://7ragnarok7.github.io/DEDMAP/",
        "Bug Tracker": "https://github.com/7Ragnarok7/DEDMAP/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
