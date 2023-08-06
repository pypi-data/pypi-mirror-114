import os

from setuptools import setup, find_packages

def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()

setup(
    name='pybancodobrasil',
    version='0.0.2',
    url='https://github.com/guifabrin/pubancodobrasil',
    author='Guilherme Fabrin Franco',
    author_email='guilherme.fabrin@gmail.com',
    license='MIT',
    include_package_data=True,
    package_data={'pybancodobrasil': ['src/*']},
    install_requires=['setuptools', 'requests', 'wget', 'jsmin', 'selenium'],
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ]
)