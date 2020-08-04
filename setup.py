import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="lyrics_extractor",
    version="3.0.1",
    description="Get Lyrics for any songs by just passing in the song name (spelled or misspelled) in less than 2 seconds using this awesome Python Library.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/Techcatchers/PyLyrics-Extractor",
    author="Rishabh Agrawal",
    author_email="rishabha.1999@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["lyrics_extractor"],
    include_package_data=True,
    install_requires=["requests", "beautifulsoup4", "lxml"],
    extras_require={
        'dev': [
            'python-dotenv',
        ]
    },
    entry_points={
        "console_scripts": [
            "lyrics_extractor=lyrics_extractor.lyrics:SongLyrics",
        ]
    },
)