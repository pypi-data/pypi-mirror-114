=========
zeit.msal
=========

Helper to authenticate against Microsoft Azure AD and store the resulting tokens for commandline applications.

Usage
=====

1. Run interactively to store a refresh token in the cache
2. Use in e.g. automated tests to retrieve an ID token from the cache (which automatically refreshes it if necessary).

::

    $ msal-token --client-id=myclient --client-secret=mysecret \
        --cache-url=file:///tmp/msal.json login
    Please visit https://login.microsoftonline.com/...
    # Perform login via browser


    def test_protected_web_ui():
        auth = zeit.msal.Authenticator(
            'myclient', 'mysecret', 'file:///tmp/msal.json')
        http = requests.Session()
        http.headers['Authorization'] = 'Bearer %s' % auth.get_id_token()
        r = http.get('https://example.zeit.de/')
        assert r.status_code == 200


Alternatively, retrieve the refresh token after interactive login, and use that in tests::

    auth.login_with_refresh_token('myrefreshtoken')
