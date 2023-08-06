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

To install from source:

```
# install virtualenv
pip install virtualenv

# creating a virtual environment
virtualenv env_automatiic

#if the above does not work, try the following:
python -m virtualenv env_automatiic

# activate the virtual environment
source env_automatiic/bin/activate

# clone package from GitHub
git clone git@github.com:cs107-califour/cs107-FinalProject.git

# navigate to the appropriate folder
cd cs107-FinalProject

# install the requirements for automatiic
pip install -r requirements.txt

# navigate to test_suite folder to run tests
pytest test_math.py 

# leave virtual environment
deactivate 
```
