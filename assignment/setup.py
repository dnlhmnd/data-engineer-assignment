from setuptools import setup

with open ("README.md", encoding="utf-8") as readme_file:
    readme = readme_file.read()

setup(
    name="assignment",
    description="Assignment for Data Engineer role application at OneByZero",
    author="Daniel Hammond",
    author_email="danielhammond1999@gmail.com",
    long_description=readme
)