from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'A basic package that allows you to spam text!'
LONG_DESCRIPTION = 'A basic package that allows you to spam text, with or without sending it/pressing enter.'

# Setting up
setup(
    name="spam-yo-friends",
    version=VERSION,
    author="Cxstin",
    author_email="<dobrecostindragos@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['keyboard', 'pyautogui', 'questionary'],
    keywords=['python', 'spam', 'spamming', 'message spamming', 'message spam'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)