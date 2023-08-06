from __future__ import print_function
from setuptools import setup

setup(
    name="haostart",
    version="1.0.1",
    author="haostart",
    author_email="haostart@hotmail.com",
    description="Haostart-Self",
    long_description=open("README.md", encoding='utf-8').read(),
    license="Apache License",
    url="https://gitee.com/haostart/dashboard/projects",
    packages=['haostart'],
    install_requires=[
        'requests',
        'simplejson',
        'opencv-python',
    ],
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Text Processing :: Indexing",
        "Topic :: Utilities",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python",

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.8',
    ],
)
