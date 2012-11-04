import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'nltk',
    'numpy',
    'bottle',
    'jinja2',
    ]

setup(name='LiteralPainting',
      version='0.0',
      description='A natural language processing tool to draw on a canvas.',
      long_description=README + '\n\n' +  CHANGES,
      classifiers=[
        "Programming Language :: Python",
        ],
      author='',
      author_email='',
      url='',
      keywords='nltk',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='LiteralPainting',
      install_requires=requires,
      )

