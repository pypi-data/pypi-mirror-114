import os
from functools import wraps

from flask import _request_ctx_stack, session, request

AUTH0_DOMAIN = os.environ.get('AUTH0_DOMAIN')
API_AUDIENCE = os.environ.get('AUTH0_API_AUDIENCE')
ALGORITHMS = ["RS256"]

class AuthApp():
    _instance = None

    def __init__(self, app):
        self.app = app

    @classmethod
    def get(cls):
        if not cls._instance:
            raise Exception('No app set')
        return cls._instance.app

    @classmethod
    def set(cls, app):
        cls._instance = AuthApp(app)

class AppError(Exception):
    ERROR_CODE = None
    ERROR_DESCRIPTION = None
    def __init__(self, error):
        self.error = error
        self.status_code = self.ERROR_CODE

class AuthError(AppError):
    ERROR_CODE = 401
    ERROR_DESCRIPTION = "Unauthorized"

class BadRequestError(AppError):
    ERROR_CODE = 400
    ERROR_DESCRIPTION = "Bad Request"

def get_current_user():
    user_token = _request_ctx_stack.top.current_user
    return user_token.get('sub')

# Format error response and append status code
def get_token_auth_header():
    """Obtains the Access Token from the Authorization Header
    """
    with AuthApp.get().app_context():
        auth = request.headers.get("Authorization", None)
        if not auth:
            raise AuthError({"code": "authorization_header_missing",
                            "description":
                                "Authorization header is expected"})

        parts = auth.split()

        if parts[0].lower() != "bearer":
            raise AuthError({"code": "invalid_header",
                            "description":
                                "Authorization header must start with"
                                " Bearer"})
        elif len(parts) == 1:
            raise AuthError({"code": "invalid_header",
                            "description": "Token not found"})
        elif len(parts) > 2:
            raise AuthError({"code": "invalid_header",
                            "description":
                                "Authorization header must be"
                                " Bearer token"})

        token = parts[1]
        return token

def get_payload():
    token = get_token_auth_header()
    jsonurl = urlopen("https://"+AUTH0_DOMAIN+"/.well-known/jwks.json")
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    for key in jwks["keys"]:
        if key["kid"] == unverified_header["kid"]:
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"]
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer="https://"+AUTH0_DOMAIN+"/"
            )
        except jwt.ExpiredSignatureError:
            raise AuthError({"code": "token_expired",
                            "description": "token is expired"}, 401)
        except jwt.JWTClaimsError:
            raise AuthError({"code": "invalid_claims",
                            "description":
                                "incorrect claims,"
                                "please check the audience and issuer"}, 401)
        except Exception:
            raise AuthError({"code": "invalid_header",
                            "description":
                                "Unable to parse authentication"
                                " token."}, 401)
        return payload
    raise AuthError({"code": "invalid_header",
                    "description": "Unable to find appropriate key"}, 401)

def requires_auth(f):
    """Determines if the Access Token is valid
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        payload = get_payload()
        _request_ctx_stack.top.current_user = payload
        session['current_user'] = payload
        return f(*args, **kwargs)
    return decorated

def requires_scope(required_scope):
    """Determines if the required scope is present in the Access Token
    Args:
        required_scope (str): The scope required to access the resource
    """
    token = get_token_auth_header()
    unverified_claims = jwt.get_unverified_claims(token)
    if unverified_claims.get("scope"):
            token_scopes = unverified_claims["scope"].split()
            for token_scope in token_scopes:
                if token_scope == required_scope:
                    return True
    return False