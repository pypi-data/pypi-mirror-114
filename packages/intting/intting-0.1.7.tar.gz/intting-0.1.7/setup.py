import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="intting",
  version="0.1.7",
  author="zjy_090820",
  author_email="a1234567890001919@outlook.com",
  description="easy to user int (beta)",
  long_description='This packge can help you to ctrl int better,and we will to hard to update the packge!',
  url="https://pypi.org",
  include_package_data=True,
  packages=setuptools.find_packages(),
  classifiers=[
  "Programming Language :: Python :: 3",
  "License :: OSI Approved :: MIT License",
  "Operating System :: OS Independent",
  ],
)