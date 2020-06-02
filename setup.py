import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cutefluffyfox",
    version="0.1",
    author="cutefluffyfox",
    author_email="mishkazel1@mail.ru",
    description="Python library for writing applications on yandex voice assistant",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cutefluffyfox/pyalice",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
