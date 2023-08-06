import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="exeLauncher",
    version="1.0.0",
    author="Fruitsy",
    description="All this does is launch .exe files directly from the command prompt, lol.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=[],
    python_requires=">=3.6",
)