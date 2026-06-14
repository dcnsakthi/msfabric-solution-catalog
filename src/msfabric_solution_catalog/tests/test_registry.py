"""Tests for catalog registry validation."""

import logging
import re
import shutil
import subprocess
from pathlib import Path

import pytest
import yaml
from pydantic import ValidationError

from .schemas import catalog as CatalogSchema

logger = logging.getLogger(__name__)


def get_registry_path() -> Path:
    """Get the path to the catalogs directory."""
    return Path(__file__).parent.parent / "msfabric_solution_catalog" / "catalogs"


def load_registry_data() -> list:
    """Load raw registry data from YAML files in catalogs directory."""
    registry_path = get_registry_path()
    catalogs = []
    
    # Load from core folder
    core_dir = registry_path / "core"
    if core_dir.is_dir():
        for yml_file in sorted(core_dir.glob("*.yml")):
            with open(yml_file, 'r', encoding='utf-8') as f:
                catalog = yaml.safe_load(f)
                if catalog:
                    catalog['core'] = True
                    catalogs.append(catalog)
    
    # Load from community folder
    community_dir = registry_path / "community"
    if community_dir.is_dir():
        for yml_file in sorted(community_dir.glob("*.yml")):
            with open(yml_file, 'r', encoding='utf-8') as f:
                catalog = yaml.safe_load(f)
                if catalog:
                    catalog['core'] = False
                    catalogs.append(catalog)
    
    return catalogs


def validate_catalog_config(catalog_data: dict) -> dict | None:
    """Validate a single catalog config.
    
    Args:
        catalog_data: A single catalog dict to validate
        
    Returns:
        Validated catalog dict or None if invalid.
    """
    catalog_id = catalog_data.get('logical_id', '[unknown]')
    
    try:
        validated = CatalogSchema(**catalog_data)
        logger.debug(f"catalog '{catalog_id}' validated successfully")
        return validated.model_dump()
    except ValidationError as e:
        logger.warning(
            f"catalog '{catalog_id}' filtered out due to schema validation error: {e}"
        )
        return None


class TestRegistryValidation:
    """Test suite for registry schema validation."""

    def test_registry_file_exists(self):
        """Verify catalogs directory exists."""
        registry_path = get_registry_path()
        assert registry_path.exists(), f"catalogs directory not found at {registry_path}"
        assert registry_path.is_dir(), f"catalogs path must be a directory at {registry_path}"

    def test_registry_is_valid_yaml(self):
        """Verify registry.yml is valid YAML."""
        registry_data = load_registry_data()
        assert isinstance(registry_data, list), "Registry should contain a list of catalogs"

    def test_all_catalogs_have_valid_schema(self):
        """Verify all catalogs in registry pass schema validation."""
        registry_data = load_registry_data()
        
        invalid_catalogs = []
        for catalog_data in registry_data:
            catalog_id = catalog_data.get('logical_id', '[unknown]')
            try:
                CatalogSchema(**catalog_data)
            except ValidationError as e:
                invalid_catalogs.append((catalog_id, str(e)))
        
        if invalid_catalogs:
            error_messages = [f"  - {jid}: {err}" for jid, err in invalid_catalogs]
            pytest.fail(
                "The following catalogs failed schema validation:\n" + 
                "\n".join(error_messages)
            )

    @pytest.mark.parametrize("catalog_data", load_registry_data(), ids=lambda j: j.get('logical_id', 'unknown'))
    def test_individual_catalog_schema(self, catalog_data):
        """Test each catalog individually for better error reporting."""
        catalog_id = catalog_data.get('logical_id', '[unknown]')
        try:
            validated = CatalogSchema(**catalog_data)
            assert validated.logical_id == catalog_id
        except ValidationError as e:
            pytest.fail(f"catalog '{catalog_id}' failed validation: {e}")

    def test_ids_are_unique_and_positive(self):
        """Ensure numeric ids are unique and positive across the registry."""
        registry_data = load_registry_data()
        id_to_logical = {}
        for j in registry_data:
            jid = j.get('id')
            lid = j.get('logical_id', '<unknown>')
            assert isinstance(jid, int) and jid > 0, f"id must be a positive integer for '{lid}' (got {jid!r})"
            if jid in id_to_logical:
                pytest.fail(f"Duplicate id {jid} found in '{lid}' and '{id_to_logical[jid]}'")
            id_to_logical[jid] = lid

    def test_logical_ids_are_unique(self):
        """Ensure logical_ids are unique across the registry."""
        registry_data = load_registry_data()
        seen = {}
        for j in registry_data:
            lid = j.get('logical_id')
            assert lid, f"logical_id must be present (id={j.get('id')})"
            if lid in seen:
                pytest.fail(f"Duplicate logical_id '{lid}' (ids: {seen[lid]} and {j.get('id')})")
            seen[lid] = j.get('id')

    def test_logical_ids_are_kebab_case(self):
        """Ensure logical_ids are lowercase kebab-case (pipe case)."""
        registry_data = load_registry_data()
        slug_re = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
        for j in registry_data:
            logical_id = j.get('logical_id')
            assert logical_id is not None, "logical_id must be present"
            assert slug_re.match(logical_id), f"logical_id '{logical_id}' must be kebab-case (lowercase letters/numbers with dashes)"

    def test_repo_urls_and_refs_resolve(self):
        """Ensure remote repo_url/repo_ref pairs are reachable via git ls-remote."""
        if not shutil.which("git"):
            pytest.skip("git executable not available")

        registry_data = load_registry_data()
        for j in registry_data:
            source = j.get("source", {}) or {}
            repo_url = source.get("repo_url")
            if not repo_url:
                continue

            repo_ref = source["repo_ref"]
            check_cmd = ["git", "ls-remote", "--exit-code", repo_url, repo_ref]
            result = subprocess.run(check_cmd, capture_output=True, text=True, timeout=15)

            if result.returncode == 0:
                continue

            # If the ref lookup failed, check if the repo itself is reachable to
            # distinguish a bad ref from a network/auth issue.
            reachability = subprocess.run(
                ["git", "ls-remote", "--exit-code", repo_url],
                capture_output=True,
                text=True,
                timeout=15,
            )

            if reachability.returncode != 0:
                pytest.skip(
                    f"Unable to reach repo_url '{repo_url}' (logical_id={j.get('logical_id', '[unknown]')}); "
                    f"stderr: {reachability.stderr.strip()}"
                )

            assert False, (
                f"Repo ref not reachable for {j.get('logical_id', '[unknown]')}: {repo_url}@{repo_ref}\n"
                f"stderr: {result.stderr.strip()}"
            )
        slug_re = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
        for j in registry_data:
            logical_id = j.get('logical_id')
            assert logical_id is not None, "logical_id must be present"
            assert slug_re.match(logical_id), f"logical_id '{logical_id}' must be kebab-case (lowercase letters/numbers with dashes)"

    def test_validate_catalog_config_returns_dict_on_success(self):
        """Test validate_catalog_config returns dict for valid config."""
        valid_config = {
            "id": 999,
            "logical_id": "test-catalog",
            "name": "Test catalog",
            "description": "A test catalog",
            "date_added": "01/01/2025",
            "workload_tags": ["Test"],
            "scenario_tags": ["Test"],
            "source": {"workspace_path": "/src",},
            "entry_point": "1_ExploreData.Notebook",
            "owner_email": "owner@example.com",
        }
        result = validate_catalog_config(valid_config)
        assert result is not None
        assert result['logical_id'] == "test-catalog"

    def test_validate_catalog_config_returns_none_on_failure(self):
        """Test validate_catalog_config returns None for invalid config."""
        invalid_config = {
            "id": "missing-required-fields"
            # Missing required fields
        }
        result = validate_catalog_config(invalid_config)
        assert result is None

    def test_core_flag_based_on_folder(self):
        """Verify core flag is set correctly based on folder location."""
        registry_data = load_registry_data()
        
        # All catalogs should have core flag
        for catalog in registry_data:
            logical_id = catalog.get('logical_id', '[unknown]')
            assert 'core' in catalog, f"catalog '{logical_id}' missing core flag"
            assert isinstance(catalog['core'], bool), f"catalog '{logical_id}' core flag must be boolean"

    def test_yaml_filenames_match_logical_ids(self):
        """Ensure each YAML filename matches the logical_id inside it."""
        registry_path = get_registry_path()
        for folder in ("core", "community"):
            folder_path = registry_path / folder
            if not folder_path.is_dir():
                continue
            for yml_file in sorted(folder_path.glob("*.yml")):
                with open(yml_file, "r", encoding="utf-8") as f:
                    data = yaml.safe_load(f)
                if not data:
                    continue
                logical_id = data.get("logical_id")
                expected = yml_file.stem
                assert logical_id == expected, (
                    f"Filename '{yml_file.name}' does not match logical_id '{logical_id}' "
                    f"(expected logical_id to be '{expected}')"
                )

    def test_diagram_svgs_exist(self):
        """Verify every catalog with a mermaid_diagram has light and dark SVGs in assets."""
        diagrams_dir = Path(__file__).resolve().parent.parent.parent.parent / 'assets' / 'images' / 'diagrams'
        registry_data = load_registry_data()

        missing = []
        for catalog in registry_data:
            if not catalog.get('mermaid_diagram'):
                continue
            logical_id = catalog.get('logical_id', '<unknown>')
            for variant in ('light', 'dark'):
                svg_path = diagrams_dir / f"{logical_id}_{variant}.svg"
                if not svg_path.exists():
                    missing.append(f"{logical_id}_{variant}.svg")

        if missing:
            pytest.fail(
                "Missing diagram SVGs in assets/images/diagrams/:\n"
                + "\n".join(f"  - {f}" for f in missing)
            )

    def test_workload_tag_images_exist(self):
        """Verify every workload tag used in scenarios has a corresponding image in shared assets."""
        shared_assets = Path(__file__).resolve().parent.parent.parent.parent / 'assets' / 'images' / 'tags' / 'workload'
        image_extensions = ('.svg', '.png', '.jpg', '.jpeg', '.webp')
        registry_data = load_registry_data()

        all_tags = set()
        for catalog in registry_data:
            for tag in catalog.get('workload_tags', []):
                all_tags.add(tag)

        missing = []
        for tag in sorted(all_tags):
            slug = re.sub(r'[^a-z0-9]+', '-', tag.lower()).strip('-')
            if not any((shared_assets / f"{slug}{ext}").exists() for ext in image_extensions):
                missing.append(tag)

        if missing:
            pytest.fail(
                "Missing images for workload tags in assets/images/tags/workload/:\n"
                + "\n".join(f"  - {tag}" for tag in missing)
            )




