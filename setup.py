from setuptools import setup, find_packages
from pathlib import Path

HERE = Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name="solobot-web-api",
    version="1.0.1",
    packages=find_packages(),
    install_requires=[
        "aiohttp>=3.8.0",
    ],
    python_requires=">=3.9",
    description="Async Python SoloBot API Wrapper",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/hteppl/solobot-web-api",
    author="hteppl",
    author_email="hteppl.dev@gmail.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
    ],
    include_package_data=True,
)
