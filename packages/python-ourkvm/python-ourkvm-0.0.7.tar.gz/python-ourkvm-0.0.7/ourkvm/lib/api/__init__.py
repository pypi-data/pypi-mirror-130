import urllib.error
from fastapi import Depends, FastAPI
from typing import Dict, Any
from .user import User as User
from ...storage import storage

if storage['arguments'].api:
	from .app import app as app
	from .helpers import get_current_user as get_current_user
	from .networking import get_network_interface_info
	from .qemu import create_machine_configuration

	@app.get("/users/me")
	def get_current_user_information(current_user: User = Depends(get_current_user)) -> User:
		"""
		This API call will return the current (logged in) user information.
		"""
		return current_user

	@app.get("/clusters")
	def list_all_known_cluster_nodes(current_user: User = Depends(get_current_user)) -> Dict[str, Any]:
		"""
		List all available clusters (if any).
		"""
		return {}

	import sys
	# Avoid running uvicorn if pytest is being executed.
	if "pytest" not in sys.modules:
		import uvicorn
		uvicorn.run(app)