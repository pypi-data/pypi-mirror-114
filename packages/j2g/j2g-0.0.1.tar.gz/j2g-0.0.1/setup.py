from setuptools import setup, find_packages

import j2g

setup(
    name="j2g",
    version=j2g.__version__,
    author=j2g.__author__,
    author_email=j2g.__author__,
    packages=find_packages(),
    install_requires=['graphviz'],
    license='MIT',
    url=j2g.__url__,
)
