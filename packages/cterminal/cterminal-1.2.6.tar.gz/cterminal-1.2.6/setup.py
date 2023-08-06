from setuptools import setup
import pathlib

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="cterminal",
    version="1.2.6",
    description="Colored Prints for python",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/novus-alex/PyProgress",
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
