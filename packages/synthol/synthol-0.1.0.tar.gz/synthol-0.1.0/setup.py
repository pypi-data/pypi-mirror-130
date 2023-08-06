import sys
from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="synthol",
    version="0.1.0",
    description="Simple Python3 dependency injector",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Red Balloon Security",
    url="https://gitlab.com/redballoonsecurity/synthol",
    packages=[
        "synthol",
    ],
    ext_modules=[],
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Topic :: Software Development",
    ],
    license_files=["LICENSE"],
    install_requires=["typing_inspect"] + (
        ["dataclasses"] if sys.version_info < (3, 7) else []
    ),
    python_requires=">=3",
    project_urls={
        "Bug Tracker": "https://gitlab.com/redballoonsecurity/synthol/-/issues",
    },
)
