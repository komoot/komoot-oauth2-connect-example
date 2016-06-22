# komoot-oauth2-connect-example
Example application to connect to komoot via oauth2

This feature is currently a private beta.

## Run it locally

 - Fork or clone the project
 - Create a python virtual environment ```virtualenv --distribute -p python3 .env```
 - Activate the virtual environment ```. .env/activate.fish``` (for the fish shell)
 - Install dependencies ```pip install -r requirements.txt```
 - Run the server application ```python test_server.py --client-id XXX --client-secret YYY````
 - Open your browser [http://localhost:5000/](localhost:5000/) and login with a regular komoot user accout (Note, during beta not all accounts are whitelisted for OAuth2).
