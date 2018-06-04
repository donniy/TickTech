# TickTech


### Dependencies
- npm & nodejs
- python3
- pip


### Installation
First make sure you have all the dependencies installed list above. The other dependencies
will be managed using pip.

If you can run a bash script on your machine you can use the INSTALL script.
This script creates a virtualenv called venv and install the required dependencies
using pip.

At the moment it does not install the vue dependencies, because of an error on the frontend
which should be fixed. The install file will be uploaded then.

If you cannnot run a bash script then follow the next steps

--change directory to app/frontend
--run npm install
--run npm run build
--change directory back to the head folder, so back two levers.
--create a virtual environment (virtualenv venv). In the gitingore files are some names for the
environment directory names we ignore. Dont upload your virtual environment directory to git!
activate the virtualenv
pip install -r requirements.txt

That are all the steps needed for installation.

### Running
In order to run the app, start your virtual environment.
Then run flask within your virtual environment. For running flask check the docs.


### Documentation
 - Flask: https://flask.pocoo.org/docs/1.0
 - Vue: https://vuejs.org/v2/guide
