from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.4'
DESCRIPTION = 'This package is made by me, means Abhinav Mishra'
LONG_DESCRIPTION = 'A package to perform arithmetic operations, in-build Text-to-speech program, Auto alert gui box and lots more. To download this module, go to your cmd(Command Prompt) or terminal and type the command given at the top. Hope you will like it!!'

# Setting up
setup(
    name="Abhinav",
    version=VERSION,
    author="Abhinav Mishra",
    author_email="abhinavkrishu007@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['arithmetic', 'math', 'mathematics', 'pyautogui', 'pyttsx3', 'best', 'python', 'abhicoder','abhinav mishra', 'abhinav'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)