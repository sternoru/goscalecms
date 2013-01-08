import ez_setup
import os
ez_setup.use_setuptools()
from setuptools import setup, find_packages

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

setup(
    name = "goscalecms",
    version = "0.1",
    packages = find_packages(),
    author = "Evgeny Demchenko",
    author_email = "little_pea@list.ru",
    description = "GoScale CMS",
    long_description = README,
    url = "https://bitbucket.org/littlepea12/goscale/",
    include_package_data = True,
    install_requires = [
        "unidecode",
        "feedparser",
        "gdata",
        "Django >= 1.1.1",
        "django-cms >= 2.2",
    ]
)