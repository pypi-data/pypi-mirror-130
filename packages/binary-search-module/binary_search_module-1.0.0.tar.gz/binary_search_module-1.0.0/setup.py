from setuptools import setup, find_packages


setup(
    name="binary_search_module",
    version="1.0.0",
    description="Package of binary search method",
    author="Kirill Borisyuk",
    author_email="hurricanekba@gmail.com",
    packages=find_packages(include=['project', 'project.*']),
)
