from setuptools import setup, find_packages
import codecs
import os

VERSION = '1.0.1'
DESCRIPTION = 'Installs my jarvis code on your system'
LONG_DESCRIPTION = 'A package to install Jarvis on your system'

# Setting up
setup(
    name="jarviswithgui",
    version=VERSION,
    author="Aditya Garg",
    author_email="adityagarg1165@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['pyttsx3','speechrecognition','wikipedia','Pyqt5','Pyqt5-tools','pyjokes','pyautogui'],
    keywords=['Jarvis', 'jarviswithgui', 'gui', 'python', 'aditya'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ]
)