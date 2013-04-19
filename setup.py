import os
import imp

try:
    imp.find_module('setuptools')
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()

from setuptools import setup, find_packages

README = open('README.rst').read()

setup(
    name = "goscalecms",
    version = __import__('goscale').__version__,
    packages = find_packages(),
    author = "Evgeny Demchenko",
    author_email = "little_pea@list.ru",
    description = "GoScale CMS is an extension of Django CMS. It's a set of unique plugins and useful tools for Django CMS that makes it very powerful by seamlessly integrating content from 3rd party websites to make mashups.",
    long_description = README,
    license = "BSD",
    keywords = "goscale cms django themes content management system mashup google ajax",
    url = "https://github.com/sternoru/goscalecms",
    include_package_data = True,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Internet :: WWW/HTTP :: Site Management",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Natural Language :: French",
        "Natural Language :: Russian",
        "Programming Language :: Python",
        "Programming Language :: JavaScript",
        "License :: OSI Approved :: BSD License",
    ],
    install_requires = [
        "pytz",
        "unidecode",
        "BeautifulSoup",
        "feedparser",
        "gdata",
        "python-dateutil",
        "simplejson",
        "Django>=1.4,<1.6",
        "django-cms==2.4",
    ]
)
