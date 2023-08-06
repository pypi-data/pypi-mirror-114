from msal.token_cache import decode_id_token
from time import time
from urllib.parse import urlparse, parse_qsl
import msal
import wsgiref.simple_server
import zeit.msal.cache


class Authenticator:

    redirect_url = 'http://localhost:4180/oauth2/callback'
    tenant_zeitverlag = 'f6fef55b-9aba-48ae-9c6d-7ee8872bd9ed'

    def __init__(self, client_id, client_secret, cache, tenant_id=None,
                 scopes=None):
        if isinstance(cache, str):
            cache = zeit.msal.cache.from_url(cache)
        self.cache = cache
        if tenant_id is None:
            tenant_id = self.tenant_zeitverlag
        self.app = msal.ConfidentialClientApplication(
            client_id, client_secret, token_cache=self.cache,
            authority='https://login.microsoftonline.com/%s' % tenant_id)
        # msal requires this to signify that we want an ID token. It then
        # allows specifying no other scopes, but implicitly uses openid,profile
        # So I guess we're lucky that we use `upn` and not `mail`, because I
        # don't see a way to add the `email` scope here.
        if scopes is None:
            self.scopes = [client_id]
        else:
            self.scopes = scopes

    def get_id_token(self):
        self.cache.load()
        accounts = self.app.get_accounts()
        if not accounts:
            raise RuntimeError('No cached token available')

        # XXX The msal cache currently does not handle id tokens, it always
        # runs refresh even if the cached data is still valid.
        result = self.cache.find(self.cache.CredentialType.ID_TOKEN)
        if result:
            token = result[0]['secret']
            try:
                data = decode_id_token(token)
            except Exception:
                pass
            else:
                # Like _acquire_token_silent_from_cache_and_possibly_refresh_it
                expires_in = data['exp'] - time()
                if expires_in > 5 * 60:
                    return token

        result = self.app.acquire_token_silent(self.scopes, accounts[0])
        if not result:
            raise RuntimeError('Refreshing token failed')
        self.cache.save()
        return result['id_token']

    def get_access_token(self):
        self.cache.load()
        accounts = self.app.get_accounts()
        if not accounts:
            raise RuntimeError('No cached token available')
        result = self.app.acquire_token_silent(self.scopes, accounts[0])
        if not result:
            raise RuntimeError('Refreshing token failed')
        self.cache.save()
        return result['access_token']

    def login_with_refresh_token(self, token):
        result = self.app.acquire_token_by_refresh_token(token, self.scopes)
        if 'error' in result:
            raise RuntimeError(result['error'])
        self.cache.save()
        return result['id_token']

    login_result = None

    def login_interactively(self):
        self.flow = self.app.initiate_auth_code_flow(
            self.scopes, self.redirect_url)
        print('Please visit %s' % self.flow['auth_uri'])
        self.accept_http_callback()
        if not self.login_result:
            raise RuntimeError('Obtaining token failed')
        self.cache.save()
        return self.login_result['id_token']

    def accept_http_callback(self):
        with wsgiref.simple_server.make_server(
                '0.0.0.0', urlparse(self.redirect_url).port,
                self.http_callback,
                handler_class=SilentRequestHandler) as server:
            server.handle_request()

    def http_callback(self, environ, start_response):
        start_response('200 OK', [('Content-type', 'text/plain')])
        self.login_result = self.app.acquire_token_by_auth_code_flow(
            self.flow, dict(parse_qsl(environ.get('QUERY_STRING', ''))))
        return [b'Success, this window can now be closed']


class SilentRequestHandler(wsgiref.simple_server.WSGIRequestHandler):

    def log_request(self, *args, **kw):
        pass
