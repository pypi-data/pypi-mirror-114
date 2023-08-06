import pathlib

from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent
# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name='teko-import-test',
    description='A simple commandline app for import test cases from .xlsx file',
    version='0.2',
    py_modules=['cli'],
    install_requires=[
        'Click',
        'openpyxl',
        'pandas'
    ],
    entry_points='''
        [console_scripts]
        teko-import-test=cli:cli
    ''',
    author="Anh Nguyen Viet",
    author_email='anhvietnguyen.nva@gmail.com',
    keyword="teko, import, test",
    long_description=README,
    long_description_content_type="text/markdown",
)