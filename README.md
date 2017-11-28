# miot
middleware for IOT devices based on RESTful web API

## To use this project

* Configuration
```
	$ sudo apt-get install python3 python-pip
	$ sudo pip install virtualenv virtualenvwrapper
		Se estiver usando Pip3:
		echo "export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3" >> ~/.bashrc
	$ echo "export WORKON_HOME=~/Env" >> ~/.bashrc
	$ echo "source /usr/local/bin/virtualenvwrapper.sh" >> ~/.bashrc
	$ source ~/.bashrc
	$ mkvirtualenv redes_proj (or anything else you want)
```
* Dependencies

```
	CLONE PROJECT FROM GIT
	$ pip install -r requirements.txt
```

* Run Project
```
	$ python3 miot.py
```