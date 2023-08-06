from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='column_print',
    version='0.0.1',
    author="Steve Daulton",
    author_email="steve.daulton@gmail.com",
    url="https://github.com/SteveDaulton/column_print",
    description='Terminal print strings in columns',
    long_description=long_description,
    long_description_content_type="text/markdown",
    py_modules=["column_print"],
    package_dir={'': 'src'},

    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.0",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Topic :: Printing",
        "Topic :: Terminals",
        ],

    extras_require = {
        "dev": [
            "pylint>=2.4.4",
            "check-manifest>=0.40",
            "sphink>=1.3",
        ],
    },
    platforms=[
        "Linux",
    ],
    license="GNU General Public License v2 or later (GPLv2+)",
)
