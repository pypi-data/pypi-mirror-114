import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="imgkerneliu",
    version="0.0.2",
    author="ken",
    author_email="liuyunclouder@gmail.com",
    description="Image kernel.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/liuyunclouder/imgkerneliu",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
