# TickTech


### Dependencies
- npm & nodejs
- python3
- pip


### Installation
First make sure you have all the dependencies installed listed above. The other dependencies
will be managed using pip.

If you can run a bash script on your machine you can use the INSTALL script.
This script creates a virtualenv called venv and install the required dependencies
using pip.

At the moment it does not install the vue dependencies, because of an error on the frontend
which should be fixed. The install file will be uploaded then.

If you cannnot run a bash script then follow the next steps

First change the directory to app/frontend

'''sh
cd app/frontend
'''

Then run npm commands to setup vuejs

'''sh
npm install
npm run build
'''

Then move back to the base directory
'''sh
cd ../../
'''

Setup a virtual environment, for the name we use venv, if you want to use a different one
check the gitignore file for possible names, or add the name to gitignore. Do not update your
virtual environment directory to git!

'''sh
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
'''
That are all the steps needed for installation.

### Running
In order to run the app, start your virtual environment.

'''sh
source venv/bin/activate
'''

Then execute these commands from the project root, to run flask and the application.
'''sh
export FLASK_ENV=development
FLASK_APP=app/backend/app.py flask run
'''

To deactivate your virtual environment do:
'''sh
deactivate
'''

### Documentation
 - Flask: https://flask.pocoo.org/docs/1.0
 - Vue: https://vuejs.org/v2/guide
