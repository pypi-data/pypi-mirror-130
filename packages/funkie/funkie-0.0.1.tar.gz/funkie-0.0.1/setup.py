
import setuptools
  
with open("README.md", "r") as fh:
    description = fh.read()
  
setuptools.setup(
    name="funkie",
    version="0.0.1",
    author="RobertCodedIt",
    author_email="robertlove999999@gmail.com",
    packages=["funkie"],
    description="A sample test package",
    long_description=description,
    long_description_content_type="text/markdown",
    url="https://github.com/robertCodedIt/misc-pkg",
    license='MIT',
    python_requires='>=3.8',
    install_requires=[]
)