from setuptools import setup, find_packages

# set __version__, https://stackoverflow.com/a/16084844/14012992
__version__ = None
exec(open('tepezza/__version__.py').read()) 
assert __version__, "version not set in __version__.py"

setup(
    name='tepezza',
    version=__version__,
    author = 'Will Bradley',
    author_email = 'derivativedude123@gmail.com',
    description = ('Scrape doctor data from www.tepezza.com'),
    long_description = open('README.md').read(),
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/2435191/TepezzaScraper',
    project_urls = {
        'Bug Tracker': 'https://github.com/2435191/TepezzaScraper/issues'
    },
    classifiers = [
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    packages=find_packages(),
    include_package_data=True,
    package_data = {
        "tepezza": ["data/*"]
    }
)