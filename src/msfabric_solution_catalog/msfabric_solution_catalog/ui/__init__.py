"""UI components for Fabric catalog.

This module contains all UI rendering components:
- catalog: catalog catalog list display
- install_status: Installation status cards
- formatting: Code syntax highlighting
- conflict_resolver: Conflict detection and resolution UI
"""

from .catalog import render_catalog_list, reload_assets
from .install_status import render_install_status_html
from .conflict_resolver import ConflictDetector, ConflictResolver, ConflictUI
from .formatting import render_copyable_code, syntax_highlight_python

__all__ = [
    'render_catalog_list',
    'reload_assets',
    'render_install_status_html',
    'ConflictDetector',
    'ConflictResolver',
    'ConflictUI',
    'render_copyable_code',
    'syntax_highlight_python',
]

