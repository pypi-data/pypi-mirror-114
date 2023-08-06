import pathlib
import setuptools

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setuptools.setup(
    name="canonical-phone",
    version="0.0.9",
    author="Amit Saraswat",
    author_email="amit.saraswat@pasarpolis.com",
    description="Library to get canonical phone number",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/pasarpolis/canonical-phone.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    license="MIT",
    include_package_data=True,
    install_requires=[],
)
