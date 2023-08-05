from pathlib import Path
from setuptools import find_packages, setup


def get_major(line: str, major: int) -> int:
    if "major" in line:
        major = int(line.rsplit("=", 1)[1])
    return major


def get_minor(line: str, minor: int) -> int:
    if "minor" in line:
        minor = int(line.rsplit("=", 1)[1])
    return minor


def get_patch(line: str, patch: int) -> int:
    if "patch" in line:
        patch = int(line.rsplit("=", 1)[1])
    return patch


# PEP 440, Pre-releases:
# Alpha release: aN
# Beta release: bN
# Release Candidate: rcN
# Where N stands for sequential number of pre-release.
def get_pre_release(line: str, pre_release: str) -> str:
    if "pre_release" in line:
        pre_release = str(line.rsplit("=", 1)[1])
    return pre_release


def get_version() -> str:
    major = 0
    minor = 0
    patch = 0
    pre_release = None
    with open(Path(__file__).parent.joinpath("VERSION")) as version_file:
        for line in version_file:
            line = line.strip()
            major = get_major(line, major)
            minor = get_minor(line, minor)
            patch = get_patch(line, patch)
            pre_release = get_pre_release(line, pre_release)
    return str(major) + "." + str(minor) + "." + str(patch) + pre_release


def get_readme() -> str:
    with open(Path(__file__).parent.joinpath("README.md")) as readme_file:
        readme = readme_file.read()
    return readme


def get_requirements_list() -> list:
    with open(Path(__file__).parent.joinpath("requirements.txt")) as requirements_file:
        requirements_list = requirements_file.read().splitlines()
    return requirements_list


setup(name="fasta-splitter",
      version=get_version(),
      description="Command line tool to split one multiple sequences fasta file into individual sequences fasta files.",
      long_description=get_readme(),
      long_description_content_type="text/markdown",
      url="https://github.com/alan-lira/fasta-splitter",
      author="Alan Lira",
      author_email="",
      license="MIT",
      platforms=["Operating System :: MacOS",
                 "Operating System :: Microsoft :: Windows :: Windows 10",
                 "Operating System :: POSIX :: Linux"],
      classifiers=["Development Status :: 2 - Pre-Alpha",
                   "Intended Audience :: Developers",
                   "Intended Audience :: End Users/Desktop",
                   "Intended Audience :: Science/Research",
                   "License :: OSI Approved :: MIT License",
                   "Natural Language :: English",
                   "Operating System :: MacOS",
                   "Operating System :: Microsoft :: Windows :: Windows 10",
                   "Operating System :: POSIX :: Linux",
                   "Programming Language :: Python :: 3.6",
                   "Programming Language :: Python :: 3.7",
                   "Programming Language :: Python :: 3.8",
                   "Programming Language :: Python :: 3.9",
                   "Topic :: Scientific/Engineering :: Bio-Informatics"],
      packages=find_packages(),
      include_package_data=True,
      install_requires=get_requirements_list(),
      entry_points={"console_scripts": ["fastasplitter=main:main_group"]})
