import setuptools

with open("equirc/README.md", "r") as fh:
    long_description = fh.read()

requirements = []

setuptools.setup(
    name="equirc",
    version="1.0.0",
    author="Vincent Mallet, Jean-Philippe Vert",
    author_email="vincent.mallet96@gmail.com",
    description="Reverse Complement Equivariant Layers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Vincentx15/Equi-RC",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)