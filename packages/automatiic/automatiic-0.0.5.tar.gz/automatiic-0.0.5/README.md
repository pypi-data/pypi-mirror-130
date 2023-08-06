[![Build Status](https://app.travis-ci.com/cs107-califour/cs107-FinalProject.svg?token=haghCcKiJxBbTrUunAR2&branch=main)](https://app.travis-ci.com/cs107-califour/cs107-FinalProject)


[![codecov](https://codecov.io/gh/cs107-califour/cs107-FinalProject/branch/main/graph/badge.svg?token=W0FG925728)](https://codecov.io/gh/cs107-califour/cs107-FinalProject)

# cs107-FinalProject

## Group 30 

| Name      | Email |
| ----------- | ----------- |
| Austin Nguyen | austinnguyen@g.harvard.edu  |
| Emma Besier  | emmabesier@g.harvard.edu    |
| Lottie Zhuang  | luoting_zhuang@hms.harvard.edu    |
| Hainan Xiong   | hainanxiong@hsph.harvard.edu        |


## Installation

We have two approaches to installation. We recommend the <code>virtualenv</code> approach because which it helps isolate Python installations and contains a Python interpreter, a pip executable and a site-packages directory. Ultimately, this makes it easier for users whose version of Python they are running their scripts with is not configured to search for modules where they have installed them.

**Option 1:** Install package using <code>pip install automatiic</code>. 

**Option 2:** Create virtual environment and clone the git repository.

1. Install virtualenv: <code>pip install virtualenv</code>

2. Creating a virtual environment: <code>virtualenv env_automatiic</code> or <code>python -m virtualenv env_automatiic</code>

3. Activate the virtual environment: <code>source env_automatiic/bin/activate</code>

4. Clone package from GitHub: <code>git clone git@github.com:cs107-califour/cs107-FinalProject.git</code>

5. Navigate to the appropriate folder: <code>cd cs107-FinalProject</code>

6. Install the requirements for automatiic: <code>pip install -r requirements.txt</code>

7. (Optional) Run tests for automatiic using the test suite: <code>pytest test_suite/test_forward.py</code> <code>pytest test_suite/test_reverse.py</code>

8. Leave virtual environment after using the package: <code>deactivate</code>

## Broader Impact and Inclusivity Statement
Automatic differentiation, and the packages that implement it, have played a transformative role in optimization, neural networks, computer vision, natural language processing, and probabilistic inference. In almost every way, automatic differentiation outperforms its alternatives: manual differentiation is time consuming and prone to error, numerical differentiation can be highly inaccurate due to round-off and truncation errors, and symbolic differentiation often results in complex expressions.

But with its power also comes risk. Autodifferentiation packages such as automatiic are prone to misuse and can play an important role in malicious projects, such as the generation of deepfakes, AI-supported password guessing, and human impersonation. The ease-of-use of differentiation packages such as automatiic may also encourage people to opt for a more complicated and less-interperatable solution like a neural network, over something simpler like a regression model. To use our package and others like it, one should consider: 1) the social implications of the task being solved (i.e. does this have the potential to harm others?), 2) whether the current use of the package is aligned with the intended use outlined in the official documentation, and 3) whether or not automatic differentiation is the best and simplest solution to the task at hand.

With respect to inclusivity, automatic differentiation as a method is more accessible to underrepresented groups than other differentiation techniques. It is understandable with a weak math background, as all numerical computations are compositions of a finite set of elementary operations. The main barrier to entry, we argue, is the technology needed to successfuly download and use the package that implements it—one must have access to a computer with sufficient speed and power, access to WiFi, and the courage to insert oneself in the arguably intimidating culture of tech. Underrepresented groups, working parents, non-English speakers and those in rural areas are most likely to be faced with these obsticles.

Even if the user has made it past the above barriers to entry, they must have their work reviewed and approved by project maintainers—who are overwhelmingly white and male. Bias, implicit or not, permeates the workplace and creates additional difficulties for already marginalized groups. While we can indeed write a "Diversity Statement" on our package website, a more proactive way of encouraging diversity in our users would be to hold workshops designed for negleted populations, and to publicly support programs that provide WiFi and computers in under-served communities.
