import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="lightningmcqueen",
    version="1.0.0",
    description="The fastest Python development experience in the galaxy",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://replit.com/@notjustinshaw/lightningmcqueen",
    author="Justin Shaw",
    author_email="realjustinshaw@gmail.com",
    license="MIT",
    packages=["lightningmcqueen"],
    include_package_data=True,
    install_requires=["replit", "flask"],
    entry_points={
        "console_scripts": [
            "start=lightningmcqueen.__main__:main",
        ]
    },
)