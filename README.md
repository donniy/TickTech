# TickTech


### Dependencies
- python3
- pip3


### Installation
First make sure you have all the dependencies, that are listed above, installed.
The other dependencies will be managed using pip.

If you can run a bash script on your machine you can use the INSTALL script.
This script creates a virtualenv called venv and install the required dependencies
using pip. If you do not want your virtual environment to be called venv, you can give an argument to the script
with the desired name. Please make sure you do not upload your virtual environment to git, so update the .gitignore file
or use a virtual environment name already specified in the envs area in the .gitignore file.

If you cannnot run a bash script then follow the next steps.

##### Setting up the virtual env.
Setup a virtual environment, for the name we use venv, if you want to use a different one
check the gitignore file for possible names, or add the name to gitignore. Do not update your
virtual environment directory to git!

```sh
virtualenv venv
source venv/bin/activate
pip3 install -r requirements.txt
```
These are all the steps needed for installation.

### Start developing
In order to run the app, start your virtual environment.
If your virtual environment is not called venv, then replace venv with your virtuel environment name.
```sh
source venv/bin/activate
```

Then execute these commands from the project root, to run flask and the application in development mode.
```sh
export FLASK_ENV=development
FLASK_APP=app/backend/app.py flask run
```

To deactivate your virtual environment do:
```sh
deactivate
```

#### Adding a python dependency
If you do not use a virtual environment, dont do this step!. Just install it locally
but dont update the requirements.txt. So if you do not use a virtual environment, DONT DO THIS!!!

If you want to add a python dependency then follow the following steps, in this example we install numpy.
Install the dependency in your virtual environment using pip.
```sh
pip install numpy
```
Then update the requirements.txt using the following command, but make sure you are in your virtual environment!
```sh
pip freeze > requirements.txt
```
Now this dependency can be easily installed by the rest, and a version can be specified upon the original installation, which
is then followed by everyone.


### Installing a python dependency
If you walk into an error, where a python library is not installed, someone probably installed a new dependency.
If they used the above method this can easily be installed with the following steps.
First make sure you are in your virtual environment.
Then run the following command:
```sh
pip install -r requirements.txt
```
If everything went well, this should update your libraries in your virtual environment, so that everything is up to
date.

### Documentation
 - Flask: https://flask.pocoo.org/docs/1.0
 - Vue: https://vuejs.org/v2/guide



 ### Canvas and LTI
 In order to test the lti integration and canvas environment we provided a docker image, filled with some test data.
 In order to use this docker image use the following commands after having your docker setup and your
 docker daemon running.
 ```sh
 docker pull tiktech/tiktech-canvas
 ```
 After pulling the image creata a container with the following command:
```sh
docker run --name canvas-docker-tiktech -p 3000:3000 -d tiktech/tiktech-canvas
```
This will create a container with the name canvas-docker-tiktech
This will run the docker, starting up might take a while.

To run the docker again, after stopping, run the following command:
```sh
docker start -i canvas-docker-tiktech
```

When your docker has fully started go to:
http://localhost:3000 or 0.0.0.0:3000 where you can login with the following credentials:
username = canvas@example.edu
and password = canvas-docker

Now you can browse courses and act as users. If u click on a course on the side will show
tiktech, if u click on tiktech a tiktech session inside lti will start.
