from os import path
from setuptools import setup, find_packages

with open("./takelessons_scraper/__version__", "r") as f:
    version = f.readline()

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

with open(path.join(this_directory, 'LICENSE'), encoding='utf-8') as f:
    license = f.read() 

requirements = [
"requests>=2.25.1",
"selenium>=3.141.0",
"pendulum>=2.1.2"
]

requirements_tests = [
    "pytest"
]


setup(
    name="takelessons-scraper",
    version=version,
    author="EliMor",
    author_email="elimor.github@gmail.com",
    description="Scrape chat content from TakeLessons.com",
    long_description=long_description,
    long_description_content_type='text/markdown',
    license=license,
    packages=['takelessons_scraper'],
    include_package_data=True,
    install_requires=requirements,
    extras_require={'tests': requirements_tests},
    test_suite="tests",
    tests_require=requirements_tests,
    classifiers=[
        # Supported Python versions
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ]
)