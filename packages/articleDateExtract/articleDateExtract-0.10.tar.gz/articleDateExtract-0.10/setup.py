from codecs import open

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open('README.md', 'r', 'utf-8') as f:
    readme = f.read()

setup(
    name='articleDateExtract',
    packages=['articleDateExtract'],
    version='0.10',
    author='Krishna Kishore',
    author_email='imwebruster@gmail.com',
    url='https://github.com/blueshirtdeveloper/article-date-extract',
    license='MIT',
    description='Automatically extracts and normalizes an online article or blog post publication date',
    long_description_content_type='text/markdown',
    long_description=readme,
    install_requires=[
        "beautifulsoup4 >= 4.9.3",
        "python-dateutil >= 2.7.3",
        "lxml >= 4.6.1"
    ],
    classifiers=(
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.8'
        )
)