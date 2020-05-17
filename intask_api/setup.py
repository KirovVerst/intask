import os
from textwrap import dedent

from setuptools import find_packages
from setuptools import setup


def _read_reqs(filename):
    file_path = os.path.join(os.path.dirname(__file__), filename)

    try:
        with open(file_path) as f:
            return [
                l.strip()
                for l in f
                if not any(l.startswith(s) for s in ("#", "-", "../"))
            ]
    except OSError:
        return ""


setup_params = dict(
    name="Intask API",
    version="0.1.0",
    description="",
    long_description="",
    author="Azat Abubakirov",
    author_email="kirov.verst@gmail.com",
    url="https://github.com/KirovVerst/intask",
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    classifiers=dedent(
        """
        Development Status :: 5 - Production/Stable
        Natural Language :: English
        Operating System :: POSIX :: Linux
        Programming Language :: Python
        Programming Language :: Python :: 3.8
        """
    )
    .strip()
    .splitlines(),
    license="Proprietary",
    keywords=[],
    platforms=["Linux"],
    include_package_data=True,
    zip_safe=False,
    install_requires=_read_reqs("requirements.txt"),
)


def main():
    setup(**setup_params)


if "__main__" == __name__:
    main()
