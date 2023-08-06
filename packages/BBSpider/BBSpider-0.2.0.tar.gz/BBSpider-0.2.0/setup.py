import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="BBSpider",
    version="0.2.0",
    author="ZzxxH",
    author_email="654245529@qq.com",
    description="a web spider",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.dailyrecords.xyz/",
    project_urls={
        "Bug Tracker": "https://www.dailyrecords.xyz/",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires = ">=3.6"
)

