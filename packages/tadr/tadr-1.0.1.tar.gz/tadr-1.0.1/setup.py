from setuptools import setup, find_packages
from core.classes import VERSION

def readme():
    return open('README.md', 'r').read()

setup(
    name="tadr",
    version=VERSION,
    scripts=["tadr"],
    author="Murdo Maclachlan",
    author_email="murdo@maclachlans.org.uk",
    description="A tool that will automatically reply done to the first 'cannot find transcription' message from the r/TranscribersOfReddit bot. ",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/MurdoMaclachlan/tadr",
    packages=find_packages(),
    install_requires=[
        "colored",
        "configparser",
        "praw>=7.1.2"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    license='GPLv3+'
)
