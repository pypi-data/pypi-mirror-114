from setuptools import setup
import pathlib

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="cterminal",
    version="1.5.0",
    description="Terminal Tools for python",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/novus-alex/cterminal",
    author="Alexandre Hachet",
    author_email="alexandrehachet1@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["cterminal"],
    include_package_data=True,
)
