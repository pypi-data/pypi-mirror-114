import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("lrtools/__init__.py") as f:
    lines = f.readlines()

for l in lines:
    if l.startswith("__version__ ="):
        version = l.split("=")[1].strip()[1:-1]

setuptools.setup(
    name="lrtools",
    version=version,
    author="Conqu3red",
    description="Python library for loading and writing Line Rider tracks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Conqu3red/trk-python",
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    install_requires=[],
)