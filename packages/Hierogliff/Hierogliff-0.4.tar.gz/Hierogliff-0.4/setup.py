"""
@author: Stella Ituze
Contains Global setup functions
"""
from setuptools import find_packages, setup

# reading long description from file
with open('README.md') as file:
    long_description = file.read()
  
# specify requirements of your package here
REQUIREMENTS = ['numpy', 'pytest']
CLASSIFIERS =[
        'Programming Language :: Python :: 3',
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
            ]
#Calling the setup function
setup (

    name='Hierogliff',
    version='0.4',
    description ='The package hierogliff performs automatic differentiation',
    long_description=long_description,
    url='https://github.com/cs107-hierogliff/cs107-FinalProject/blob/main/docs/DOCUMENTATION.md',
    author ='Stella Ituze | Kishan Venkataramu | Maxime Laasri | Lara Zeng',
    author_email= 'ituzes@college.harvard.edu',
    packages=find_packages(include=['hierogliff','hierogliff.src','hierogliff.src.node', 'hierogliff.src.node.dual','hierogliff.tests', 'hierogliff.tests.node']),
    classifiers=CLASSIFIERS,
    # Needed for dependencies
    install_requires=REQUIREMENTS,
    python_requires= ">=3.6",
)   

