from setuptools import setup,find_packages
import codecs
import os

VERSION = "1.0.0.0"
DESCRIPTION = "handtrackingmodule"
LONG_DESCRIPTION = "A package to do hand tracking using the opencv-python "
setup(
    name="HandTrackingModulevarun",
    version=VERSION,
    author="Varun Gupta",
    author_email="Varun.gupta.py@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description= LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['opencv-python'],
    keywords=["Hand Tracking Module","hand tracking module","Varun Gupta","varun gupta","opencv python","cv2","opencv"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
