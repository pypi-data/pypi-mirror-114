from setuptools import find_packages, setup
from os import path


with open('E:\my work\py_nmr_analysis\Readme.md', "r", encoding="utf-8") as fh:
    long_description = fh.read()



setup(
    name='pynmranalysis',
    packages=find_packages(include=['pynmranalysis']) ,
    version='0.6.1',
    description='python library for nmr quantification and analysis',
    long_description = long_description ,
    url="https://github.com/1feres1/pynmranalysis/",
    author='Feres',
    author_email='jjhelmus@gmail.com',
    license='MIT',
    install_requires=['numpy' , 'pandas ' ,"scipy " , "pyod == 0.9.0"
                      ],

    setup_requires=['pytest-runner'],
    tests_require=['pytest==6.2.4'],
    test_suite='tests',
)