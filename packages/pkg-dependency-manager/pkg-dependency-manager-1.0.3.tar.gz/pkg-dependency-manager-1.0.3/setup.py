from setuptools import setup, find_packages
from subprocess import Popen, PIPE
import os, os.path
print(f"cwd: {os.getcwd()}")
with open("README.md", "r", encoding="utf-8") as readme:
    long_description = readme.read()
    readme.close()
version_file_name = "version.txt"
if os.path.exists(version_file_name):
    with open(version_file_name, "r") as stream:
        latest_tag = stream.read().strip()
        stream.close()
else:
    with Popen(["git", "tag", "-l"], stdout=PIPE) as command:
        output = command.communicate()
        tags = output[0].decode("utf-8").strip().split('\n')
        latest_tag = tags[len(tags) - 1]
        with open(version_file_name, "w") as stream:
            stream.write(latest_tag)
            stream.close()
print(f"latest tag: {latest_tag}")
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