"""Setup file"""
from setuptools import setup, find_packages

# Read the contents of your requirements.txt file
with open('requirements.txt', encoding="utf-8") as f:
    requirements = f.read().splitlines()

with open('README.md', encoding="utf-8") as f:
    long_description = f.read()

setup(
    name='project_actionable_reviews',
    version='0.1',  # Update with your package version
    author='Ioana Baciu',
    author_email='ioana.iris@gmail.com',
    description='',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/IoanaBaciu24/ActionableReviews',
    packages=find_packages(),  # Automatically discover and include all packages
    install_requires=requirements,  # Use the dependencies from requirements.txt
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3.8',],
)
