import setuptools
from pathlib import Path

setuptools.setup(
    name='kshgym1',
    version='0.0.1',
    description="A OpenAI Gym Env for foo",
    long_description=Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(include="kshgym1*"),
    install_requires=['gym']

)