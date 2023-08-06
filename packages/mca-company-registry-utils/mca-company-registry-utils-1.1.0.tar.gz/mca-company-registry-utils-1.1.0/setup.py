import setuptools
from setuptools import setup

setup(
    name='mca-company-registry-utils',
    version='1.1.0',
    zip_safe=False,
    description='Ministry of Corporate affairs company registry API',
    url='https://github.com/bharath-sadhu/mca-company-registry.git',
    author='bharath sadhu',
    author_email='bharath.sadhu@cloudwick.com',
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7'
    ],
    long_description='Ministry of Corporate affairs company registry API',
    keywords='Company Registry',
    packages=setuptools.find_packages(),
    include_package_data=True,
    setup_requires=['setuptools','pytest-runner'],
    install_requires=[
         'fastapi',
         'pydantic',
         'asyncio',
         'typing'
    ],
    entry_points={}
)