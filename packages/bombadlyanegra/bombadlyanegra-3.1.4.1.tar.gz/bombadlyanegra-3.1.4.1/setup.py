from setuptools import setup, find_packages

NAME = "bombadlyanegra"
DESCRIPTION = "bomber"
URL = "https://github.com/crinny/bombadlyanegra"
EMAIL = "maxxsim.ka007@gmail.com"
AUTHOR = "skylongg"
REQUIRES_PYTHON = ">=3.7.0"
VERSION = "3.1.4.1"

with open("requirements.txt", encoding="utf-8") as f:
    REQUIRED = f.readlines()

try:
    with open("README.md", encoding="utf-8") as f:
        long_description = "\n" + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=DESCRIPTION,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=["bombadlyanegra"],
    entry_points={
        "console_scripts": ["bombadlyanegra=bombadlyanegra.cli:main", "bomber=bombadlyanegra.cli:main"]
    },
    install_requires=REQUIRED,
    extras_require={},
    package_data={"bombadlyanegra": ["services/*", "app/*", "app/*/*", "app/static/*/*"]},
    license="Mozilla Public License 2.0",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Operating System :: Android",
        "Operating System :: Microsoft :: Windows",
        "Topic :: Internet",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
    ],
)
