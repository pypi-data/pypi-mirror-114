from setuptools import setup, find_packages
import os
import re
from subprocess import Popen, PIPE

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
README_PATH = os.path.join(BASE_DIR, "README.md")
GIT_REGEX = re.compile(rb'\[(.+)\]')


def get_long_description(path, encoding='utf-8'):
    """
    Prepare long desciption for setup.py from *readme* file.
    """
    content = ""
    with open(path, encoding=encoding) as f:
        content = "\n" + f.read()
    return content


def get_last_commit_version(encoding='utf-8'):
    """
    Using subprocess.Popen read the newest commit and parse its tag. Find version between brackets, for example: [1.2.0].
    Be sure that your git way of working include such scenario.
    """
    cmd = "git log --oneline".split()
    process = Popen(cmd, stdout=PIPE, stderr=PIPE)
    output, error = process.communicate()
    last_commit_tag = output.splitlines()[0]
    g = GIT_REGEX.search(last_commit_tag)
    return g.group(1).decode(encoding)


### settings

DESCRIPTION = "Package for manipulate collections with streams and generators."

setup(
    name="py3streams",
    version=get_last_commit_version(),
    author="Adam Kyther",
    author_email="",
    desciption=DESCRIPTION,
    long_description=get_long_description(README_PATH),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'python3', 'stream', 'list', 'tuple', 'set', 'dict', 'collection'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Unix"
    ]
)

