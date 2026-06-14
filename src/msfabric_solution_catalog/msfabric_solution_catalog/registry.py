"""catalog registry management for loading and querying available catalogs."""

import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

import yaml

logger = logging.getLogger(__name__)


class catalogRegistry:
    """Manages the catalog registry and provides query operations.
    
    The registry is loaded from individual YAML files organized in core/
    and community/ subdirectories.
    """
    
    def __init__(self, registry_path: Optional[Path] = None):
        """Initialize the registry.
        
        Args:
            registry_path: Path to catalogs directory containing core/ and community/.
                          If None, uses default location: catalogs/
        """
        if registry_path is None:
            registry_path = Path(__file__).parent / "catalogs"
        self._registry_path = registry_path
        self._catalogs: Optional[List[Dict]] = None
    
    def load(self) -> List[Dict]:
        """Load the catalog registry from directory structure.
        
        Scans core/ and community/ subdirectories and adds the 'core' flag
        based on folder location.
        
        Returns:
            List of catalog configuration dictionaries
            
        Raises:
            FileNotFoundError: If catalogs directory doesn't exist
            yaml.YAMLError: If any YAML file is invalid
        """
        if self._catalogs is None:
            logger.debug(f"Loading catalog registry from {self._registry_path}")
            
            if not self._registry_path.is_dir():
                raise FileNotFoundError(
                    f"catalogs directory not found at {self._registry_path}"
                )
            
            self._catalogs = self._load_from_directory(self._registry_path)
            logger.info(f"Loaded {len(self._catalogs)} catalogs from registry")
            
        return self._catalogs
    
    def _load_from_directory(self, catalogs_dir: Path) -> List[Dict]:
        """Load catalogs from directory structure with core/community folders.
        
        Args:
            catalogs_dir: Path to catalogs directory containing core/ and community/
            
        Returns:
            List of catalog configuration dictionaries with 'core' flag added
        """
        catalogs = []
        
        # Load from core folder
        core_dir = catalogs_dir / "core"
        if core_dir.is_dir():
            for yml_file in sorted(core_dir.glob("*.yml")):
                with open(yml_file, 'r', encoding='utf-8') as f:
                    catalog = yaml.safe_load(f)
                    if catalog:
                        catalog['core'] = True
                        catalogs.append(catalog)
                        logger.debug(f"Loaded core catalog: {yml_file.name}")
        
        # Load from community folder
        community_dir = catalogs_dir / "community"
        if community_dir.is_dir():
            for yml_file in sorted(community_dir.glob("*.yml")):
                with open(yml_file, 'r', encoding='utf-8') as f:
                    catalog = yaml.safe_load(f)
                    if catalog:
                        catalog['core'] = False
                        catalogs.append(catalog)
                        logger.debug(f"Loaded community catalog: {yml_file.name}")
        
        return catalogs
    
    def get_by_id(self, catalog_id: str) -> Optional[Dict]:
        """Get a catalog by its logical_id or numeric id.
        
        Args:
            catalog_id: Logical ID (e.g., "analytics-lab") or numeric ID
            
        Returns:
            catalog configuration dict or None if not found
        """
        catalogs = self.load()
        return next(
            (
                item
                for item in catalogs
                if item.get('logical_id') == catalog_id
                or str(item.get('id')) == str(catalog_id)
            ),
            None,
        )
    
    def list_all(self, include_unlisted: bool = False) -> List[Dict]:
        """Get all catalogs, optionally filtering by listing status.
        
        Args:
            include_unlisted: If True, include catalogs with include_in_listing=False
            
        Returns:
            List of catalog configuration dictionaries
        """
        catalogs = self.load()
        if include_unlisted:
            return catalogs
        return [j for j in catalogs if j.get('include_in_listing', True)]
    
    def filter_by_workload(self, workload: str) -> List[Dict]:
        """Filter catalogs by workload tag.
        
        Args:
            workload: Workload tag to filter by (e.g., "Data Engineering")
            
        Returns:
            List of matching catalogs
        """
        catalogs = self.load()
        return [
            j for j in catalogs
            if workload in j.get('workload_tags', [])
        ]
    
    def filter_by_scenario(self, scenario: str) -> List[Dict]:
        """Filter catalogs by scenario tag.
        
        Args:
            scenario: Scenario tag to filter by
            
        Returns:
            List of matching catalogs
        """
        catalogs = self.load()
        return [
            j for j in catalogs
            if scenario in j.get('scenario_tags', [])
        ]
    
    def filter_by_type(self, catalog_type: str) -> List[Dict]:
        """Filter catalogs by type.
        
        Args:
            catalog_type: Type to filter by (e.g., "Tutorial", "Demo", "Accelerator")
            
        Returns:
            List of matching catalogs
        """
        catalogs = self.load()
        return [
            j for j in catalogs
            if j.get('type', '').lower() == catalog_type.lower()
        ]
    
    def mark_new_items(self, days_threshold: int = 60) -> List[Dict]:
        """Mark catalogs as 'new' based on their date_added.
        
        Args:
            days_threshold: Number of days to consider an item "new"
            
        Returns:
            List of all catalogs with 'is_new' field added
        """
        catalogs = self.load()
        new_threshold = datetime.now() - timedelta(days=days_threshold)
        
        for j in catalogs:
            try:
                date_added = datetime.strptime(j['date_added'], "%m/%d/%Y")
                j['is_new'] = date_added >= new_threshold
            except (ValueError, KeyError):
                j['is_new'] = False
        
        return catalogs
    
    def sort_catalogs(
        self, 
        catalogs: List[Dict], 
        new_first: bool = True
    ) -> List[Dict]:
        """Sort catalogs by newness, then ID.
        
        Args:
            catalogs: List of catalogs to sort
            new_first: If True, put new items first
            
        Returns:
            Sorted list of catalogs
        """
        return sorted(
            catalogs,
            key=lambda x: (
                not x.get('is_new', False) if new_first else x.get('is_new', False),
                x.get('id', 0),
                x.get('logical_id', '')
            )
        )
    
    def group_by_scenario(self, catalogs: List[Dict]) -> Dict[str, List[Dict]]:
        """Group catalogs by their scenario tags.
        
        Args:
            catalogs: List of catalogs to group
            
        Returns:
            Dictionary mapping scenario tags to lists of catalogs
        """
        grouped = {}
        for j in catalogs:
            scenario_tags = j.get("scenario_tags", ["Uncategorized"])
            for tag in scenario_tags:
                if tag not in grouped:
                    grouped[tag] = []
                grouped[tag].append(j)
        return grouped
    
    def group_by_workload(self, catalogs: List[Dict]) -> Dict[str, List[Dict]]:
        """Group catalogs by their primary (first) workload tag.
        
        Each catalog appears in exactly one group to avoid duplicates.
        
        Args:
            catalogs: List of catalogs to group
            
        Returns:
            Dictionary mapping workload tags to lists of catalogs
        """
        grouped = {}
        for j in catalogs:
            primary_workload = j.get("workload_tags", ["Uncategorized"])[0]
            if primary_workload not in grouped:
                grouped[primary_workload] = []
            grouped[primary_workload].append(j)
        return grouped
    
    def group_by_type(self, catalogs: List[Dict]) -> Dict[str, List[Dict]]:
        """Group catalogs by their type.
        
        Args:
            catalogs: List of catalogs to group
            
        Returns:
            Dictionary mapping types to lists of catalogs
        """
        grouped = {}
        for j in catalogs:
            type_tag = j.get("type") or "Unspecified"
            grouped.setdefault(type_tag, []).append(j)
        return grouped

