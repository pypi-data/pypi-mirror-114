#coding:utf-8
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pycodepack",
    version="1.0.2",
    author="MarxLP",
    author_email="lipi26@foxmail.com",
    description="A tiny tool to convert python files to dynamic libraries",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitee.com/Marxlp/pycodepack",
    project_urls={
        "Bug Tracker": "https://gitee.com/Marxlp/pycodepack/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "Cython",
    ],
    package_dir={"": "."},
    packages=setuptools.find_packages(where="."),
    python_requires=">=3.6",
) 
