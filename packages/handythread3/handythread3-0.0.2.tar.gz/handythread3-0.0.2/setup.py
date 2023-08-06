import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="handythread3",
    version="0.0.2",
    author="humblemat",
    author_email="humblemat@gmail.com",
    description="conversion of scipy recipy from https://github.com/scipy/scipy-cookbook from python2 to python3",
    long_description= long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/humblemat810/handythread3",
    project_urls={
        "Bug Tracker": "https://github.com/humblemat810/handythread3/projects",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.0",
)
