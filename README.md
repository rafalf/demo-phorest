### Install:
* [Python 3](https://www.python.org/downloads/release/python-363/)
* ```pip install -r requirement.txt```
* ```setupChromeOSX.sh``` (bash dir)

### Run pytest:

#### all tests
* ```pytest ./tests/ -s -v --reruns 1```   reruns set to 1 (rerun a failure once)

#### a specific test 
* ```pytest ./tests/test_demo.py::test_book_single_signup -s -v```


### Latest chrome driver:
* osx: to pull the latest driver, run ```setupChromeOSX.sh```