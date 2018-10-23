# Datascience Project: Fish Catches River Baunach

This is a small example project, where all
catched fishes are tracked in the river baunach. 


## Technologies
The project was realized with the technologies,
**MongoDB**, **Pandas**, **Plotly**, **Dash**, 
**Numpy**.


### Prerequisites
For the setup process you frist need to install 
[MongoDB](https://www.mongodb.com) on your computer.
After his step you can access to your 
MongoDB Instance with the Python module 
**pymongo**.
```
pip install pymongo
```
The configuration of this app is located in the 
_config.py_ file. Here you can setup up the name 
of your database or the name of your collection.


### Installing
For the setup process you have to run the file 
_install.py_. During this process all data points 
of the fish catches are imported to your MongoDB 
Instance.
```
python install.py
```


### Running
You can run the app with the command.
```
python index.py
```


### Author
* Initial work - First Dataset - **[Lucas Mußmächer](https://www.linkedin.com/in/lucas-muss/)**
* Datapoints - **[Angel Verein Ebern](http://www.av-ebern.de/)**
* Datapoints - **[Angel Verein Baunach](http://www.anglerverein-baunach.de)**


### Acknowledgments
* PEP8
* Raymond Hettinger