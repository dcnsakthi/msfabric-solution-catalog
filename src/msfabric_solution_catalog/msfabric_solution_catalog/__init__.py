from .core import catalog as _catalog
import os

os.environ["FABRIC_CICD_VERSION_CHECK_DISABLED"] = "1"

# Singleton instance used for convenience imports
catalog = _catalog()

__all__ = ["catalog"]


def __getattr__(name):
	"""Delegate unknown attributes to the singleton catalog instance.

	This enables patterns like:
		import msfabric_solution_catalog as js
		js.list()
	"""
	if hasattr(catalog, name):
		return getattr(catalog, name)
	raise AttributeError(f"module 'msfabric_solution_catalog' has no attribute '{name}'")


def __dir__():
	# Expose module attributes plus delegated catalog attributes
	return sorted(set(list(globals().keys()) + dir(catalog)))


