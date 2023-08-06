from setuptools import setup, find_packages

with open("info/readme.md") as f:
    LONGDESCRIPTION = f.read()

VERSION = "0.0.2"
DESCRIPTION = "mcStalker is an API wrapper for the https://mcstalker.com API. It uses efficient, asynchronous Pythonic code that's easy to use and integrate, well documented, and is modular."

# Setting up
setup(
    name="mcStalker",
    version=VERSION,
    author="TheOnlyWayUp",
    author_email="thedarkdraconian@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONGDESCRIPTION,
    packages=find_packages(),
    install_requires=["asyncio", "aiohttp", "json"],
    keywords=[
        "async",
        "aiohttp",
        "better_than_sync",
        "mcstalker",
        "minecraft",
        "server_scanning",
        "api_wrapper",
        "minecraft_server",
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
)
