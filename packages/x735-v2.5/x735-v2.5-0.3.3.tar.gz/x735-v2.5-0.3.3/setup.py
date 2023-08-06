import setuptools

# read the contents of your README file
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

git_url = "https://github.com/shitikovkirill/x735-v2.5"

setuptools.setup(
    name="x735-v2.5",
    version="0.3.3",
    description="Library for board x735",
    author="sh.kiruh@gmail.com",
    install_requires=[
        "pigpio==1.78",
        "RPi.GPIO==0.7.0",
        "click==8.0.1",
    ],
    extras_require={"dev": ["pre-commit"]},
    python_requires=">=3.7",
    packages=["x735"],
    entry_points={
        "console_scripts": ["x735fan=x735.main:fan"],
    },
    url=git_url,
    download_url="{}/archive/refs/heads/main.zip".format(git_url),
    long_description=long_description,
    long_description_content_type="text/markdown",
)
