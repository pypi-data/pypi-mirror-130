"""
MIT License

Copyright (c) 2021 RPS

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
from setuptools import setup, find_packages
import re

with open("src/reqwests/__init__.py") as f:
    version = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE
    ).group(1)

requirements = []
with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="reqwests",
    version=version,
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    project_utls={
        "Documentation": "https://reqwests.rtfd.io",
        "Issue Tracker": "https://github.com/RPSMain/reqwests/issues",
        "Pull Request Tracker": "https://github.com/RPSMain/reqwests/pulls",
    },
    url="https://github.com/RPSMain/reqwests",
    license="MIT",
    author="RPS",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    install_requires=requirements,
    description="Pythonic API Wrapper For Discord And Anime Enjoyers",
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 1 - Planning",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Framework :: AsyncIO",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
)
