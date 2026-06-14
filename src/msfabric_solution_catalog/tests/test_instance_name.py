"""Tests for resolving the catalog instance name."""


def test_module_is_returned():
    """Calling the module directly should return the module name."""
    import msfabric_solution_catalog

    assert msfabric_solution_catalog._get_instance_name() == "msfabric_solution_catalog"


def test_module_alias_is_returned():
    """Calling via module alias should return that alias (e.g., js)."""
    import msfabric_solution_catalog as js

    assert js._get_instance_name() == "js"


def test_aliased_alias_is_returned():
    """Calling via a re-aliased alias should return the new variable name."""
    import msfabric_solution_catalog as js

    js2 = js
    assert js2._get_instance_name() == "js2"


