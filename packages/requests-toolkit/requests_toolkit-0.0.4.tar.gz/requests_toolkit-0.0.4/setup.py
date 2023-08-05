from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='requests_toolkit',
    version='0.0.4',
    description='Decorators and other tools for handling common patterns with the python requests module.',
    py_modules=["requests_toolkit.json_tools"],
    package_dir={'': 'src'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        "requests ~= 2.26.0",
    ],
    extras_require={
        "dev": [
            "pytest >= 6.2.4",
        ]
    },
    url="https://github.com/benjaminCallaghan/requests_toolkit",
    author="benjaminCallaghan",
    author_email="benjamin.r.callaghan@gmail.com",
)
