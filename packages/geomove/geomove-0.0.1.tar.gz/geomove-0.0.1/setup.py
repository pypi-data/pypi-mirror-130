from os import path
import setuptools

# Collect additional information from separate files
dir = path.abspath(path.dirname(__file__))
with open(path.join(dir, "requirements.txt"), encoding="utf-8") as fp:
    install_requires = fp.read()
with open(path.join(dir, "version.txt"), encoding="utf-8") as fp:
    version = fp.readline().strip()
with open(path.join(dir, "README.md"), encoding="utf-8") as fp:
    readme = fp.read()

# Actual setup
setuptools.setup(
    name="geomove",
    description="Moves points on earth's surface towards a given bearing by a given distance.",
    long_description=readme,
    long_description_content_type="text/markdown",
    version=version,
    author="Marius Merschformann",
    author_email="marius.merschformann@gmail.com",
    url="https://github.com/merschformann/geomove",
    packages=["geomove"],
    install_requires=install_requires,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: GIS",
    ],
)
