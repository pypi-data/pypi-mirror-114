from setuptools import setup, find_packages

VERSION = '0.0.8' 
DESCRIPTION = 'API client for boring stonks'

# Setting up
setup(
        name="boringstonks", 
        version=VERSION,
        author="Kevin Per",
        author_email="kevin.per@protonmail.com",
        description=DESCRIPTION,
        packages=["boringstonks"],
        install_requires=['pandas', 'requests', 'flatten_json'],
        keywords=['python'],
)
