import json
import search_me
from configparser import ConfigParser
from setuptools import setup

config = ConfigParser()
config.read("setup.ini")

with open(config["FILES"].get("README"), "r", encoding="UTF-8") as f:
    readme = f.read()

with open(config["FILES"].get("DEPENDENCIES")) as f:
    requirements = (f.read()).split("\n")[:-1]

with open(config["FILES"].get("KEYWORDS")) as f:
    keywords = json.load(f)

with open(config["FILES"].get("CLASSIFIERS")) as f:
    classifiers = json.load(f)

setup(
    name=config["PACKAGE"].get("NAME"),
    version=search_me.__version__,
    packages=[config["PACKAGE"].get("PATH")],
    url=config["PACKAGE"].get("URL"),
    license=search_me.__license__,
    author=search_me.__author__,
    author_email=search_me.__email__,
    description=config["PACKAGE"].get("DESC"),
    long_description=readme,
    long_description_content_type=config["PACKAGE"].get("MIME"),
    install_requires=requirements,
    python_requires=config["PACKAGE"].get("PYTHON"),
    zip_safe=False,
    keywords=(keywords),
    classifiers=classifiers
)
