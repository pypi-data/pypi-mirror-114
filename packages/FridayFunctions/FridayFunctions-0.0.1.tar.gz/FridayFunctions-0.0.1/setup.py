from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'only for the use of the Author'
LONG_DESCRIPTION = "A PACKAGE FOR THE PERSONAL USE OF THE OWNER PLEASE DON'T USE IT. JUST FOR THE FUN SAKE. ALTHOGHT IT CONATINS ALL THE IMPORTANT FUCTIONS AND COLASSES FOR THE USE OF A 'PYTHON DESKTOP ASSISTANT'"

# Setting up
setup(
    name="FridayFunctions",
    version=VERSION,
    author="Sreejan",
    author_email="sreejan10246@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages('pyaduio', 'speech_recognition', 'pyttsx3'),
    install_requires=[],
    keywords=['Personal', 'Sreejan', 'Friday'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)