import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="LibraryH",
  version="0.1.0",
  author="zjy_090820",
  author_email="a1234567890001919@outlook.com",
  description="give you a better experience",
  url="https://pypi.org",
  packages=setuptools.find_packages(),
  classifiers=[
  "Programming Language :: Python :: 3",
  "License :: OSI Approved :: MIT License",
  "Operating System :: OS Independent",
  ],
)