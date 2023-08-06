#! /usr/bin/env python
import setuptools

setuptools.setup(
    name="arx-cli",
    version="0.0.1-beta",
    description="Variables, everywhere!",
    keywords="cli",
    author="Rahul Jha",
    author_email="rj722@protonmail.com",
    url="https://github.com/rj722/arx-cli",
    license="MIT",
    classifiers=[
        'Development Status :: 3 - Alpha',
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Quality Assurance",
    ],
    install_requires=["asciimatics", "typer"],
    entry_points={"console_scripts": ["arx = arx_cli.cli:app"]},
    python_requires=">=3.6",
    packages=setuptools.find_packages(exclude=["tests"]),
    package_data={"arx": ["arx_cli/sprites/*"]},
)
