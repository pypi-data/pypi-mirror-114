from distutils.core import setup
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.rst"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="capmonster_python",
    version="1.3.2",
    packages=["capmonster_python"],
    url="https://github.com/alperensert/capmonster_python",
    download_url="https://github.com/alperensert/capmonster_python/archive/1.3.2.tar.gz",
    long_description=long_description,
    license="MIT",
    author="Alperen Sert",
    author_email="alperenssrt@gmail.com",
    description="capmonster.cloud library for Python",
    requires=["requests"],
    classifiers=["Programming Language :: Python :: 3.4"]
)