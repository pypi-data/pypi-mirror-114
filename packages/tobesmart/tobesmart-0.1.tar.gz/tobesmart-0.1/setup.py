import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="tobesmart",
  version="0.1",
  author="Sheng Fan",
  author_email="fredtools999@gmail.com",
  description="Just a package that makes your python3 smart.",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/fred913",
  packages=setuptools.find_packages(),
  classifiers=[
  "Programming Language :: Python :: 3",
  "License :: OSI Approved :: MIT License"
  ],
)