from setuptools import setup, find_packages
import codecs
import os


VERSION = '0.0.2'
DESCRIPTION = 'Library for NLP data'

# Setting up
setup(
    name="doughnut",
    version=VERSION,
    author="Abdulsalam Bande",
    license='MIT',
    author_email="<abdulsalambande@gmail.com>",
    description=DESCRIPTION,
    download_url = 'https://github.com/abdulsalam-bande/doughnut/archive/refs/tags/0.0.2.tar.gz',
    url = 'https://github.com/abdulsalam-bande/doughnut',
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'numpy', 'nlp', 'machine learning'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)