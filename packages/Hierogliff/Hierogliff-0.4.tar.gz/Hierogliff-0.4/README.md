# Hierogliff

Travis CI badge:

[![Build Status](https://app.travis-ci.com/cs107-hierogliff/cs107-FinalProject.svg?token=UU1ixNUB1PZVaMyCB72B&branch=main)](https://app.travis-ci.com/cs107-hierogliff/cs107-FinalProject)

CodeCov badge:

[![codecov](https://codecov.io/gh/cs107-hierogliff/cs107-FinalProject/branch/main/graph/badge.svg?token=XFDRB6GCBG)](https://codecov.io/gh/cs107-hierogliff/cs107-FinalProject)

Hierogliff is a Python package for auto-differentiating multi-variate functions. It has minimal dependency (only uses `numpy`), and provides a user-friendly interface for defining and derivating functions.

## Functionalities

Our package supports real-valued functions defined on real-valued variables. It supports the following built-in functions: power to a positive real, exp, log, sin, cos, tan.

## Want to use our package?

Before using our package, we recommend reading the documentation provided in the `docs` folder as a `Documentation.ipynb` Jupyter Notebook file. Once you get to know the basics of how to use our package, feel free to try it out on a few of our examples!

# Contact

This package has been implemented, tested, documented, and deployed by the Group 6 of the CS107 class 2021:

- Kishan Venkataramu (kishan_venkataramu@g.harvard.edu)
- Maxime Laasri (mlaasri@g.harvard.edu)
- Stella Ituze (ituzes@college.harvard.edu)
- Lara Zeng (lzeng@college.harvard.edu)

# Broader Impact and Inclusivity Statement

### How is your software inclusive to the broader community?

Development of code has historically been, and remains, inaccessible to many groups of people, whether they are considered minorities or otherwise precluded from creating software contributions. As such, it is critical to consciously eliminate barriers to software wherever possible, and to create code and development practices that are specifically inclusive to marginalized communities. As a development team, we held a meeting at the beginning of the development process to agree on what principles we would abide by to  By hosting our package on PyPI and GitHub, by creating extensive documentation and designing our package to be as easy to use as possible, and by creating open-source software under the MIT License, we seek to maximize the reach and the inclusivity of our project. Differences in implementation ideas must be resolved through thoughtful and unbiased discussion, which may be put to a blind majority vote. We require that all developers treat each other with respect, basic decency, and kindness: this includes, but is not limited to, using correct names and pronouns, refraining from hateful or discriminatory speech, and abiding by laws and ethics. Our documentation is written in English and may be spoken aloud by an e-reader or increased in size for the visually impaired, or translated for non English speakers. 


Land Acknowledgement
This project was developed at Harvard University. Harvard University is located on the traditional and ancestral land of the Massachusett, the original inhabitants of what is now known as Boston and Cambridge. We pay respect to the people of the Massachusett Tribe, past and present, and honor the land itself which remains sacred to the Massachusett People.

### Potential broader impacts and implications 

We will be regularly responsive to any groups of people who would like to use or contribute to our package. In order to contribute to hierogliff, pull requests may be made by anyone, and will be approved under blind review without discrimination based on the original developer’s ethnicity, race, origin, creed, religion, sex, gender, or sexual orientation. To ensure that this process is fair and welcoming to all groups, mediation may be given by a third party. We have listed our contact information in our documentation and welcome emails from anyone with questions or concerns, which we will address promptly. In addition, we actively seek out feedback on accessibility from a wide range of groups, while being careful not to put the burden of representation on individuals. Should demand exceed our capabilities, we will create a forum that addresses any concerns and implement changes based on these concerns within three months, which will be staffed by the original developers. This time scale will only be changed if deemed unrealistic for the specific change requested. 

There are both benefits and risks to our package. Automatic differentiation is a powerful tool that can be used in a variety of fields, wherever essential calculations such as linear approximations, Newton’s method, tangents and normals to a curve, and minimum and maximum values are needed. Some fields, for example, are measuring earthquake magnitudes in seismology, finding profit and loss in business, and simulations and derivations in physics. Notably, our package may be used in machine learning & optimization problems, such as in solving a gradient descent problem. There is the possibility, also, that this package may be used in a neural network that gives biased or discriminatory results. Another potential negative use case is if there are any unforeseen accuracy errors in our calculations. If this particular aspect of our package is wrong, then there could be possible negative side effects: inaccuracy could result in training at a suboptimal point, which could output non-meaningful values which could have wide-reaching consequences in a healthcare setting and impact people’s lives. These are risks of open source projects which we seek to mitigate. We require all projects to strive to fulfill ethical considerations and fairness, including but not limited to the Embedded Ethics principles at Harvard University. For more information, please visit https://embeddedethics.seas.harvard.edu/.
