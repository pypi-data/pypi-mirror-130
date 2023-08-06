import urllib
from fastapi import Security
from fastapi_resource_server import JwtDecodeOptions, OidcResourceServer
from typing import Dict, Any
from .user import User
from ...storage import storage

try:
	auth_scheme = OidcResourceServer(
		f"http://{storage['arguments'].auth_server}:8080/auth/realms/{storage['arguments'].auth_realm}",
		scheme_name=storage['arguments'].auth_schema,
		jwt_decode_options=JwtDecodeOptions(verify_aud=False),
	)
except urllib.error.URLError as err:
	auth_scheme = None
	print(f"Warning: Could not initiate auth schema http://{storage['arguments'].auth_server}:8080/auth/realms/{storage['arguments'].auth_realm}: {err}")

def get_current_user(claims: Dict[str, Any] = Security(auth_scheme)) -> User:
	claims.update(username=claims["preferred_username"])
	user = User.parse_obj(claims)
	return user