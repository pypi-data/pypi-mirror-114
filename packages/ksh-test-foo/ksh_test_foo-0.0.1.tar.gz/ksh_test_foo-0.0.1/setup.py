import setuptools
from pathlib import Path

setuptools.setup(
    name='ksh_test_foo',
    version='0.0.1',
    description="A OpenAI Gym Env for foo",
    long_description=Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(include="gym_foo*"),
    install_requires=['gym']  # And any other dependencies foo needs
)