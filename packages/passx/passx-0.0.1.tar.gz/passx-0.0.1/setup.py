from setuptools import setup, find_packages

with open("requirement.txt") as f:
        install_requires = f.read().splitlines()

VERSION = '0.0.1'
DESCRIPTION = 'A Password manager using GNUPG'
LONG_DESCRIPTION = 'A package that allows you to encrypt your package using two key encryption'

# Setting up
setup(
    name="passx",
    version=VERSION,
    author="floppy04 <Harsh Baliyan>",
    author_email="<harshbaliyan126@gmail.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=install_requires,
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
