from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / 'README.md').read_text()

setup(
    name='nsystems',
    version='0.4.0',
    packages=find_packages(),
    description='Convert numbers between different numeral systems.',
    author='nsystems',
    author_email='nsystems.module@gmail.com',
    license='MIT',
    keywords=['number', 'systems', 'system', 'base', 'base64', 'base32', 'basen', 'convert', 'number systems', 'number system', 'binary', 'hexadecimal', 'octal', 'decimal'],
    long_description=long_description,
    long_description_content_type='text/markdown'
)