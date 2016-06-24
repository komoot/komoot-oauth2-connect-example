# komoot-oauth2-connect-example
Example application to connect to komoot via oauth2

This feature is currently in private beta.

## Run it locally

 1. (Fork and) clone the project.
 1. Create a python virtual environment ```virtualenv --distribute -p python3 .env```
 1. Activate the virtual environment ```. .env/activate.fish``` (for the fish shell) or ```. .env/activate``` (bash)
 1. Install dependencies ```pip install -r requirements.txt```
 1. Run the server application ```python test_server.py --client-id XXX --client-secret YYY````
 1. Open your browser [http://localhost:5000/](localhost:5000/) and login with a regular komoot user accout (Note, during beta not all accounts are whitelisted for OAuth2).
