<p align="center">
  <img src="https://github.com/dcnsakthi/msfabric-solution-catalog/raw/main/src/msfabric_solution_catalog_web/public/MSFabricSolutionCatalog.svg" alt="Microsoft Fabric Solution Catalog logo" width="300">
</p>

<p align="center">
  <a href="https://pypi.org/project/msfabric-solution-catalog/">
    <img src="https://img.shields.io/pypi/v/msfabric-solution-catalog" alt="PyPI version">
  </a>
  <a href="https://pypi.org/project/msfabric-solution-catalog/">
    <img src="https://img.shields.io/pypi/pyversions/msfabric-solution-catalog" alt="Python versions">
  </a>
</p>

<p align="center">
  <br />
  Fabric catalog accelerates Microsoft Fabric adoption with ready-to-run accelerators, demos, and tutorials that install directly into your workspace in minutes via
  <a href="https://microsoft.github.io/fabric-cicd/latest/">fabric-cicd</a>.
</p>

## Install the Library

Requirements: Python 3.10–3.13 and access to a Microsoft Fabric workspace.

```bash
pip install msfabric-solution-catalog
```

## List and Install a catalog

Run inside a Fabric notebook (or any Python environment with Fabric credentials):

```python
import msfabric_solution_catalog as catalog

# Renders an interactive catalog
catalog.list()

# Copy the install command from the catalog, past in another cell and run!
catalog.install("stateful-streaming-lakehouse")
```

Notes
- `workspace_id` is optional when you run in a Fabric notebook; it auto-detects the current workspace. Specify to deploy to another target workspace.
- `install()` accepts extras like `item_prefix` and `unattended=True` if you prefer console logs over HTML output.
- catalogs that include file upload configuration will automatically upload small data files to a Lakehouse's Files area after deployment — no extra arguments needed.

## Handling Name Conflicts

If items with the same name already exist in your workspace, Fabric catalog will detect conflicts and provide resolution options:

1. **Overwrite existing items**:
   ```python
   catalog.install("spark-structured-streaming", overwrite=True)
   ```

2. **Auto-generate a prefix** to avoid conflicts:
   ```python
   catalog.install("spark-structured-streaming", auto_prefix_on_conflict=True)
   ```
   This generates a prefix like `js3_sss__` (catalog ID + abbreviated name) and applies it to all deployed items.

3. **Provide a custom prefix**:
   ```python
   catalog.install("spark-structured-streaming", item_prefix="demo_")
   ```

The prefixing strategy:
- Renames item directories (e.g., `MyNotebook.Notebook` → `js3_sss__MyNotebook.Notebook`)
- Updates all references to renamed items within configuration files
- Uses word-boundary matching to avoid double-prefixing if you re-run the same install
- Reuses existing prefixes from previous attempts to prevent `js3_sss__js3_sss__` patterns

## Testing a catalog Before Registration

Use `_install_from_github()` to test a catalog directly from a GitHub repo before adding it to the registry. This method builds a synthetic config from the arguments you provide and runs the same install pipeline as `install()`.

```python
import msfabric_solution_catalog as catalog

catalog._install_from_github(
    logical_id="my-catalog", # sets name of root folder that items are deployed to
    repo_url="https://github.com/my-org/my-repo",
    repo_ref="v1.0.0",                           # tag or commit SHA — not a branch
    workspace_path="my-catalog/",              # defaults to "{logical_id}/"
    entry_point="GettingStarted.Notebook",
    items_in_scope=["Lakehouse", "Notebook"],
    workspace_id="<guid>",                       # target workspace (auto-resolves to the current ws in Fabric)
)
```

Common optional parameters:

```python
catalog._install_from_github(
    logical_id="my-catalog",
    repo_url="https://github.com/my-org/my-repo",
    repo_ref="abc1234",
    entry_point="GettingStarted.Notebook",
    items_in_scope=["Lakehouse", "Notebook", "SQLEndpoint"],
    workspace_path="my-catalog/",              # defaults to "{logical_id}/"
    name="My catalog",                         # display name (defaults to logical_id)
    workspace_id="<guid>",                       # target workspace (auto-detected in Fabric)
    files_source_path="my-catalog/data/",      # upload binary/data files after deploy
    files_destination_lakehouse="MyLakehouse",   # target Lakehouse for file upload
    files_destination_path="raw/",               # destination path in Lakehouse Files
    item_prefix="test_",                         # prefix all deployed item names
    unattended=True,                             # console output instead of HTML
)
```

Once the catalog installs successfully, add a YAML file to `msfabric_solution_catalog/catalogs/` and switch to the standard `catalog.install()` flow.

## Contributing

See the [root contributing guide](../../CONTRIBUTING.md) for shared guidelines (commit conventions, issue workflow, PR process), then follow the [Python library contributing guide](CONTRIBUTING.md) for development setup, quality checks, and the new catalog workflow.



