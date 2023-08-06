import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name="mf-gitvars",
    version="1.1.7",
    author="Adrian Mummey",
    author_email="adrian@momentfeed.com",
    description="A tool to parse CI/CD variables from Gitlab API",
    long_description=README,
    long_description_content_type="text/markdown",
    packages=["gitvars"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    install_requires=["python-gitlab", "colorama"],
    entry_points={
        "console_scripts": [
            "mf-gitvars=gitvars.__main__:main",
        ]
    },
)
