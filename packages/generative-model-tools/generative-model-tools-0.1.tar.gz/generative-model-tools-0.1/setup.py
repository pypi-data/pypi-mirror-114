# coding:utf-8

import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="generative-model-tools",
  version="0.1",
  author="dlzhou",
  author_email="zhou-dongliang@outlook.com",
  description="For generative models visualization",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://dlzhou.top/pypi/generative-model-tools.html",
  packages=setuptools.find_packages(),
  classifiers=[
  "Programming Language :: Python :: 3",
  "License :: OSI Approved :: MIT License",
  "Operating System :: OS Independent",
  ],
)