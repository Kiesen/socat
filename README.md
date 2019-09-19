Socat
=============
[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/Kiesen/socat/LICENSE)
[![dependencies](https://david-dm.org/Kiesen/socat.svg)](https://david-dm.org/Kiesen/socat.svg)
[![Build Status](https://travis-ci.com/Kiesen/socat.svg?branch=master)](https://travis-ci.com/Kiesen/socat)

Socat is a collection of functions to stream and analyze social media contributions.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 

### Prerequisites 

* `Python >= 3.7.2` with `pip >= 19.0.1` **(FOR LOCAL INSTALLATION WITHOUT A VIRTUALENV. NOT RECOMMENDED!)**
* `virtualenvwrapper >= 4.8.0` **(RECOMMENDED WAY IF YOU DONT WANT TO USE DOCKER)**
* `Docker >= 18.09.2` **(RECOMMENDED WAY IF YOU WANT TO USE DOCKER)**

### Installation 

#### Local without virtualenv / virtualenvwrapper

If you want to install the project without the use of virtualenv you just need to execute
```
pip install -r requirments.txt
```
which will install all required python packages. 

#### Local with virtualenv / virtualenvwrapper

If you want to install the project with the use of virtualenv or virtualenvwrapper you first need to create a new environment. For example with virtualenvwrapper you just need to execute

```
mkvirtualenv -p python3 YOUR-ENV
```

Don't forget to specify the python version `-p` if python3 is not the default version.
Then check if the environment is activate. You should see the name of your created environment on the left side of your shell.

```
(YOUR-ENV)
```

For further information, for example how to enter and leave an environment, check out the website of either [virtualenv](https://virtualenv.pypa.io/en/latest/) or [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/). Now you should able to install the packages just as mentioned before. 

```
pip install -r requirments.txt
```

This time the dependencies are saved in the environment you created before.

#### With docker

With docker you just need to run

```
docker build -t YOUR-TAG . 
```

Docker will now create an new image with all dependencies. The standard execuation behavior is to run all unittests. 
If you want to enter the docker container you could execute the following command

```
docker run -ti YOUR-TAG bash  
```

For further information how to use and create docker containers check out the website of docker.

## The socat command line interface

Socat comes with a command line interface. To see how to use it just type in:

```
python src/socat.py   
```

You should see an error message with informations about the options you could use.

### Streaming social media entries

If you want to stream social media entries you could run for example the following command

```
python src/socat.py stream tweets -m 100 -l -v  
```

which will start streaming tweets with an upper limite of 100, log and verbose mode enabled. 
The recived entries getting written to the data folder in your current working directory. If no data folder exist one will created.
For each social media source you need to put your credentials in the `.env` file. Check the `.env.example` to see how it should look like. Also check out the `config.py` inside the `stream` directory. This file is used to hand in some default parameters, in the twitter case bounding boxes, languages and words to track. 

### Analyzing social media entries or logfiles        

#### Analyze and plot logfiles

To analyze and plot logfiles just run the following command 

```
python socat.py analyze -p /path/to/logfiles logs  
```

The `-p` path option is required and needs to be an directory containing valid logfiles. You can overwrite the `PLOT_CONF` dict inside the `src/analyze/config.py` to change the log configuration.  

#### Topic detection  

To start the topic detection process just run the following command

```
python socat.py analyze -p /path/to/social_media_entries text -m KM -lang de 
```

The `-p` path option is required and needs to be an directory containing valid social media entries. There are more optional arguments like `-m` which can be used to actually run the topic detection process only with a specific methode, like k-means. Also you can prefilter the entries by a language `-lang de`. You can find a list of all supported langauges here: [langdetect](https://pypi.org/project/langdetect/). The results of the topic detection process getting printed to the stdout. Also you can overwrite the default configs of the different steps and methods. Just have a look inside the `src/analyze/config.py`.   

## Running the tests

To run all test cases, first make sure you are in the `src` directory, then just type in:

```
python -m unittest discover
```

This command executes all tests inside the `tests` directory of the `src` folder.  

## Built With

* [Python](https://www.python.org) - Python programming language 
* [pip](https://pypi.org/project/pip/) - Package installer for python
* [scikit-learn](https://scikit-learn.org/stable/) - Machine learning in python
* [langdetect](https://pypi.org/project/langdetect/) - Language detection library 
* [matplotlib](https://matplotlib.org) - Matplotlib is a Python 2D plotting library
* [Docker](https://graphql.org/learn/) - Operating-system-level virtualization (containerization)
* [argeparse](https://docs.python.org/3/library/argparse.html) - Write user-friendly command-line interfaces
* [python-dotenv](https://pypi.org/project/python-dotenv/) - Reads the .env file and adds them to environment variable

## Authors

* **Frederik Aulich** - *Initial work* - [Kiesen](https://github.com/Kiesen)

## License  

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

