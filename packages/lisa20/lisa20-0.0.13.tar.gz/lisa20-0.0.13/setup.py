import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lisa20",
    version="0.0.13",
    author="Andrew Platov",
    author_email="andrew.platow95@gmail.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
    license='Apache 2.0',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "./"},
    python_requires=">=3.6",
)