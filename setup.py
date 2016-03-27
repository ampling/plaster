import re

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = ''
with open('plasterlib/__init__.py') as f:
    version = re.search(r'^version\s*=\s*[\'"]([^\'"]*)[\'"]',
                        f.read(), re.MULTILINE).group(1)

setup(
    name = 'plaster',
    version = version,
    scripts = ['plaster'],
    packages = ['plasterlib'],

    package_dir = {
        'plasterlib': 'plasterlib'
    },

    package_data = {
        '': ['README.md'],
        'plasterlib': ['plasterlib/config', 'plasterlib/plugins/*.py']
    },
    include_package_data = True,

    author = 'Ampling',
    author_email = 'info@ampling.com',
    description = 'Adaptable command-line pastebin client',
    license = 'ISC',
    keywords = 'plaster paste bin pastebin paste-bin client command',
    url = 'https://github.com/ampling/plaster'
)
