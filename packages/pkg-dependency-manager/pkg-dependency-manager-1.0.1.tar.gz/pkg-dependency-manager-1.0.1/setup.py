from setuptools import setup, find_packages
from subprocess import Popen, PIPE
with open("README.md", "r", encoding="utf-8") as readme:
    long_description = readme.read()
    readme.close()
with Popen(["git", "describe", "--tags", "--abbrev=0"], stdout=PIPE) as command:
    output = command.communicate()
    latest_tag = output[0].decode("utf-8").strip()
setup(
    name="pkg-dependency-manager",
    version=latest_tag,
    author="ys1219",
    author_email="ys1219@cosmodash.com",
    description="A system package dependency manager, written in Python 3.9.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yodasoda1219/pkg-dependency-manager",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ],
    package_dir={"":"src"},
    packages=find_packages(where="src"),
    python_requires=">=3.9.6"
)