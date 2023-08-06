from setuptools import setup
import setuptools

with open("README.md", "r") as rm:
    long_description = rm.read()


setup(name='Morse Translator',
version='0.1',
description='Trivial Package Testing',
url='https://github.com/Tylerastro/MorseCode',
long_description=long_description,
long_description_content_type="text/markdown",
entry_points = {
    "console_scripts": [
        "morse = main.MorseDecode:main",
        ]
    },
author='Tylerastro',
python_requires='>=3',
classifiers=[
	'Development Status :: 2 - Pre-Alpha'
	],
license='MIT',
packages= setuptools.find_packages())