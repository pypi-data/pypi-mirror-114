"""
Script to publish and install taskbench and stimlib.
"""

# from distutils.core import setup
import os, pathlib
from setuptools import setup, find_packages
import taskbench

HERE = pathlib.Path(__file__).parent
README = (HERE/'README.md').read_text()
# with open('requirements.txt', 'r') as fh:
#     requirements = fh.read()

setup(
    name=taskbench.__name__,
    version=taskbench.version,
    author='Minggui Chen',
    author_email='minggui.chen@gmail.com',
    description='Behavior control software suite in Visintel lab',
    long_description=README,
    long_description_content_type='text/markdown',
    url='',
    download_url='',
    packages=find_packages(),
    include_package_data=True,
    platforms='Windows',
    # install_requires=requirements,
    classifiers=[
        'Programming Language :: Python :: 3.8',
        'License :: Other/Proprietary License',
        'Operating System :: Microsoft :: Windows'
    ],
    entry_points={
        'console_scripts': [
            'taskbench=taskbench.__main__',
        ]
    },
)
