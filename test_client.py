from requests_oauthlib import OAuth2Session
from flask import Flask, request, redirect, session, url_for
from flask.json import jsonify
import logging
import os
import argparse

app = Flask(__name__)


# This information is obtained upon registration of a new GitHub OAuth
# application here: https://github.com/settings/applications/new
client_id = None
client_secret = None
base_url = None

# must match the host and port of this application
redirect_uri = 'http://localhost:5000/callback'

@app.route("/")
def demo():
    """Step 1: User Authorization.

    Redirect the user/resource owner to the OAuth provider (komoot)
    using an URL with a few key OAuth parameters.
    """
    authorization_base_url = base_url + 'oauth/authorize'
    oauth_session = OAuth2Session(client_id, redirect_uri=redirect_uri)
    authorization_url, state = oauth_session.authorization_url(authorization_base_url)

    # State is used to prevent CSRF, keep this for later.
    session['oauth_state'] = state
    return redirect(authorization_url)


# Step 2: User authorization, this happens on the provider.

@app.route("/callback", methods=["GET"])
def callback():
    """ Step 2: Retrieving an access token.

    The user has been redirected back from the provider to your registered
    callback URL. With this redirection comes an authorization code included
    in the redirect URL. We will use that to obtain an access token.
    """

    token_url = base_url + 'oauth/token'
    oauth_session = OAuth2Session(client_id, redirect_uri=redirect_uri, state=session['oauth_state'])
    token = oauth_session.fetch_token(token_url, username=client_id, password=client_secret,
                               authorization_response=request.url)

    # At this point you can fetch protected resources but lets save
    # the token and show how this is done from a persisted token
    # in /profile.
    session['oauth_token'] = token

    return redirect(url_for('.profile'))


@app.route("/profile", methods=["GET"])
def profile():
    """ Step 3: Fetching a protected resource using an OAuth 2 token.
    """
    oauth_session = OAuth2Session(client_id, token=session['oauth_token'])

    # the username is needed for most requests and therefore in the token response
    username = session['oauth_token']['username']

    # fetch json document from main api
    response = oauth_session.get('https://external-api.komoot.de/v007/users/{}/tours/'.format(username))
    tours = response.json()
    return jsonify(tours)


if __name__ == "__main__":
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    # Enable logging of all requests: headers, bodies, responses
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True

    parser = argparse.ArgumentParser(description='komoot oauth2 test client.')
    parser.add_argument('--client-id', dest='cid', help='client id you got from komoot')
    parser.add_argument('--client-secret', dest='csecret', help='client secret you got from komoot')
    parser.add_argument('--base-url', dest='baseurl', default='https://auth.komoot.de/', help='base url for authentication requests')

    args = parser.parse_args()
    client_id = args.cid
    client_secret = args.csecret
    base_url = args.baseurl

    # Since this is a test client running on localhost: Don't enforce SSL.
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'


    os.environ['DEBUG'] = "1"
    app.secret_key = os.urandom(24)
    app.run(debug=True)
