# Data Analysis: Fish Catches River Baunach

This is a small example project, where all
catched fishes are tracked in the river baunach. 


## Technologies
The project was realized with the technologies,
MongoDB, Pandas, Plotly, Dash and Numpy.


## Prerequisites
In the first step you have to 
install a [Python Interpreter](https://www.python.org/). 
The project 
was created with Python 3.6. Additionally,
you have to install package managers, 
[Pip](https://pypi.org/project/pip/) and 
[Pipenv](https://github.com/pypa/pipenv).

### Pip Installation
```
python -m pip install --upgrade pip
pip install --upgrade setuptools
```

### Pipenv Installation
```
pip install pipenv
```

## Installing Dependencies
Run the following command to install all 
required software packages. The python packages 
(bottleneck, numexpr) require 
[Build Tools for Visual Studio](https://visualstudio.microsoft.com/de/thank-you-downloading-visual-studio/?sku=BuildTools&rel=15).
```
pipenv install -r requirements.txt
```


## Database Prerequisites
For the setup process you frist need to install 
[MongoDB](https://www.mongodb.com) on your computer.
After his step you can access to your 
MongoDB Instance with the Python package 
**pymongo**.
```
pipenv install pymongo
```
The configuration of this app is located in the 
_config.py_ file. Here you can setup up the name 
of your database or the name of your collection.


## Data Import
For the setup process you have to run the file 
install.py. During this process all data points 
of the fish catches are imported to your MongoDB 
Instance.
```
python install.py
```


## Running Dash Server
You can run the app with the command.
```
python index.py
```


## Author
* Datapoints - **[Angel Verein Ebern](http://www.av-ebern.de/)**
* Datapoints - **[Angel Verein Baunach](http://www.anglerverein-baunach.de)**
