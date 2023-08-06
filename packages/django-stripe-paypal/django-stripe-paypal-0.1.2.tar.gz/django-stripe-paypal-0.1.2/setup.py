from os import path
from setuptools import setup

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

project_urls = {
  'GitHub': 'https://github.com/botent/django-stripe-paypal',
}

setup(
    name='django-stripe-paypal',
    # other arguments omitted
    long_description=long_description,
    long_description_content_type='text/markdown',
    project_urls = project_urls
)
