from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'A Beginner Friendly Language with a syntax similar to Visual Basic and Python.'
LONG_DESCRIPTION = 'Dynamo Charlotte is a Python-based Interpreter that runs on Python Lex-Yacc Parser. It is a beginner friendly language with a syntax similar to Visual Basic and Python, allowing to create anything from numbers to multi-dimensional arrays.'

# Setting up
setup(
    name="dynamocharlotte",
    version=VERSION,
    author="Juan Carlos Juárez",
    author_email="<jc.juarezgarcia@outlook.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['Programming Language', 'Interpreter'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)