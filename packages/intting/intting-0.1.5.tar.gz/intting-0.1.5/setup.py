import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="intting",
  version="0.1.5",
  author="zjy_090820",
  author_email="a1234567890001919@outlook.com",
  description="easy to user int (beta)",
  url="https://pypi.org",
  packages=setuptools.find_packages(),
  classifiers=[
  "Programming Language :: Python :: 3",
  "License :: OSI Approved :: MIT License",
  "Operating System :: OS Independent",
  ],
)