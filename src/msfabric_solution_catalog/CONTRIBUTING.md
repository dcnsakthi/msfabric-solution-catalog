# Contributing to msfabric-solution-catalog

> Please read the [root contributing guide](../../CONTRIBUTING.md) first for shared guidelines on issues, commits, and PRs.

## Adding a New catalog

This is the most common contribution. You only need to add a single YAML file, run CI tests to validate the metadata input, and then test deploying your catalog.

1. Create a `New catalog` Issue with enough details to help maintainers determine whether the solution fits the Fabric catalog mission.
2. Community contributions are more than welcome, but we do require a Microsoft sponsor for any Core catalogs. This is someone who must have contributor level access to your project.
3. Keep catalogs self-contained: deployments must run through `catalog.install()` without manual patching.
4. Please read [STANDARDS.md](STANDARDS.md) for catalog design and quality expectations.
5. Follow the steps in [Setup of a New catalog](#setup-of-a-new-catalog) to get things set up, tested, and merged in.
5. For upgrading existing catalogs, follow the [Upgrading an Existing catalog](#updating-an-existing-catalog) guide.

## Development Setup

> **No Node.js or npm required.** The Python library is self-contained — you only need [uv](https://docs.astral.sh/uv/) (the Ruff VS Code extension is optional).

### Windows

Run from PowerShell — no WSL required:

```powershell
$GIT_ROOT = git rev-parse --show-toplevel
& "$GIT_ROOT\src\msfabric_solution_catalog\bootstrap-python.ps1"
```

This installs [uv](https://docs.astral.sh/uv/) and the following VS Code extensions: Ruff, Pylance, and Jupyter. After installation it runs `uv sync --all-groups` so you are all set to start contributing!

## Development
See the [/src/msfabric_solution_catalog/dev/test_example.ipynb](./dev/test_example.ipynb) notebook for an example of how you can interactively test your catalog.
- Develop in notebooks or `.py` files; restart the Python kernel after code changes so the notebook picks up fresh imports. Or, use `importlib` to reload specific modules for agile testing:
    ```python
    import importlib
    import msfabric_solution_catalog as catalog
    importlib.reload(catalog.core)
    importlib.reload(catalog.utils)
    importlib.reload(catalog)
    ```

## Quality Checks

Run these before submitting a PR:

```bash
cd src/msfabric_solution_catalog
uv run ruff check .                   # Lint
uv run ty check .                     # Type check
uv run pytest                         # All tests
uv run pytest tests/test_registry.py  # Registry validation (required for new catalogs)
```

## Submitting Changes

- **For new catalogs:** Create a new YAML file in `src/msfabric_solution_catalog/msfabric_solution_catalog/catalogs/community/` named `<logical-id>.yml` with all required metadata. Core catalogs (Microsoft-sponsored) go in the `core/` folder.
- Run `uv run pytest tests/test_registry.py` to confirm registry validation passes.

---

## Setup of a New catalog

1. [CORE] Create an M365 Group for the catalog owners (e.g., `fabriccatalog.spark-monitoring`). Any Core catalog needs to have multiple maintainers.
1. Create a public GitHub repo.
1. Create a Fabric Workspace named `catalog.spark-monitoring` and connect it to your GitHub repo (use a PAT with Content permissions).
1. [CORE] Make the M365 group the admin of the Fabric Workspace.
1. Populate the workspace with all items the catalog should deploy.
   - Items must be in a top-level folder named the same as the `logical_id` of the catalog (e.g., `spark-monitoring`).
   - Any data stores that need to be shared across catalogs (i.e. for modules of an overall solution like Fabric Platform Monitoring) must be stored in a top-level folder called `shared-data-stores`. Otherwise, the catalogs should self contain all Items in the single top-level folder (e.g. `spark-monitoring`).
   - Fabric items must not contain a solution prefix; catalog can optionally add an automatic prefix at deployment (e.g., `js1_sm__`) so multiple catalogs can coexist in the event of conflicting Item names. By default, no prefixing takes place, users need to opt-in to this upon being notified of Item name conflicts.
   - Do **not** use spaces in item names. Item names must either be `lower_case_snake_case` or `ProperCamelCase`. Both of these options accomodate all known naming restrictions.
   - If your catalog needs small data files uploaded to a Lakehouse's Files area, include them in the source repo and configure the `files_source_path`, `files_destination_lakehouse`, and (optionally) `files_destination_path` fields in the YAML `source` block. The upload runs automatically after item deployment.
1. Commit items to the repo.
1. Fork the msfabric-solution-catalog repo.
1. Create a new YAML file in `src/msfabric_solution_catalog/msfabric_solution_catalog/catalogs/community/` (or `core/` for Microsoft-sponsored catalogs):
   - Name the file `<logical-id>.yml` (e.g., `spark-monitoring.yml`)
   - Include all required metadata fields (see existing files for examples). _If required fields are not provided, CI tests will fail upon submission of your PR. Validate that your YAML schema conforms in advance via running `cd src/msfabric_solution_catalog && uv run pytest tests/test_registry.py`_
   - The `core` flag will be automatically set based on folder location during loading
   - Required fields (_start by copying and editing an existing YAML file_):
     - `id`: Unique positive integer (check existing IDs to avoid conflicts)
     - `logical_id`: Lowercase kebab-case identifier (e.g., `spark-monitoring`)
     - `name`: Display name
     - `description`: Max 250 characters, cannot start with the catalog name
     - `date_added`: MM/DD/YYYY format
     - `workload_tags`: List of valid workload tags
     - `scenario_tags`: List of valid scenario tags
     - `type`: One of: Tutorial, Demo, Accelerator
     - `source`: Object with `repo_url`, `repo_ref`, `workspace_path`, and optional file upload fields:
       - `files_source_path` _(optional)_: Relative path within the repo to a file or folder to upload to a Lakehouse's Files area (e.g., `retail-sales/data/`)
       - `files_destination_lakehouse` _(optional)_: Name of the target Lakehouse (must be deployed by the catalog). Required if `files_source_path` is set.
       - `files_destination_path` _(optional)_: Destination path within the Lakehouse Files area (defaults to root if omitted)
     - `items_in_scope`: List of Fabric item types in scope for deployment (e.g., Lakehouse, Notebook)
     - `entry_point`: Either a URL or `<name>.<item_type>` format
     - `owner_email`: Valid email address
1. Run `msfabric_solution_catalog.install('<logical-id>', workspace_id='<workspace_guid>')` to validate the catalog deploys correctly (see [dev_example.ipynb](../../dev/dev_example.ipynb) for a quick way to test).
1. Submit a PR with your catalog YAML file.

## Updating an Existing catalog

When a catalog's source repository publishes a new tag or ref, you can test the update before submitting a PR:

1. Use the `repo_ref` keyword argument to install with the newer ref without modifying any YAML:
   ```python
   import msfabric_solution_catalog as js
   js.install('retail-sales', workspace_id='<workspace_guid>', repo_ref='v2.0.0')
   ```
2. Validate that the catalog deploys and functions correctly with the new ref.
3. Once verified, update the `repo_ref` value in the catalog's YAML file and submit a PR.
4. Run `uv run pytest tests/test_registry.py` to confirm the new ref is reachable before pushing.

## Mermaid Diagrams

catalogs can include a `mermaid_diagram` field in their YAML file that defines a Mermaid flow diagram showing how Fabric items connect. The website renders these as pre-built SVG images (light and dark theme variants).

### Mermaid Syntax Format

Use `graph LR` (left-to-right) with `:::ClassName` annotations to specify item types:

```yaml
mermaid_diagram: |
  graph LR
    NB[spark_monitoring_setup]:::Notebook --> DP[spark_pipeline]:::DataPipeline
    DP --> ES[spark_events]:::Eventstream
    ES --> EH[spark_eventhouse]:::Eventhouse
    EH --> KDB[spark_kqldb]:::KQLDatabase
    ENV[spark_env]:::Environment -.-> NB
```

- **Node labels** (inside `[]`) should match the item name in the workspace
- **`:::ClassName`** maps the node to a Fabric item type — this determines the icon and color
- Use `-->` for solid arrows, `-.->` for dashed arrows, and `==>` for thick arrows

### Supported Item Types

| Class Name | Workload |
|------------|----------|
| `Notebook` | Data Engineering |
| `Lakehouse` | Data Engineering |
| `Environment` | Data Engineering |
| `SparkJobDefinition` | Data Engineering |
| `VariableLibrary` | Data Engineering |
| `Eventhouse` | Real-Time Intelligence |
| `Eventstream` | Real-Time Intelligence |
| `KQLDatabase` | Real-Time Intelligence |
| `KQLQueryset` | Real-Time Intelligence |
| `KQLDashboard` | Real-Time Intelligence |
| `Reflex` | Real-Time Intelligence |
| `DataPipeline` | Data Factory |
| `Dataflow` | Data Factory |
| `CopyJob` | Data Factory |
| `Warehouse` | Data Warehouse |
| `SQLEndpoint` | Data Warehouse |
| `MirroredDatabase` | Data Warehouse |
| `SQLDatabase` | SQL Database |
| `Report` | Power BI |
| `SemanticModel` | Power BI |
| `DataAgent` | Data Science |
| `MLExperiment` | Data Science |
| `UserDataFunction` | Data Science |
| `GraphQLApi` | Data Engineering |

### Emoji & Custom Icons

For nodes that aren't Fabric items (e.g., on-premise servers, external services), use a **Unicode codepoint** as the class name. The format is `U` followed by the hex codepoint (no `+`):

```yaml
mermaid_diagram: |
  graph LR
    SRV[On-Prem Server]:::U1F5A5 --> EH[eventhouse]:::Eventhouse
    DB[Legacy DB]:::U1F5C4 --> DF[ingestion]:::Dataflow
```

| Example | Codepoint | Emoji |
|---------|-----------|-------|
| `:::U1F5A5` | U+1F5A5 | 🖥 Desktop |
| `:::U1F3E2` | U+1F3E2 | 🏢 Building |
| `:::U2601`  | U+2601  | ☁ Cloud |
| `:::U1F4BB` | U+1F4BB | 💻 Laptop |
| `:::U1F5C4` | U+1F5C4 | 🗄 File Cabinet |

Emoji nodes render with the emoji in place of the Fabric icon. The item type subtitle is hidden since the codepoint isn't a meaningful label.

If a class name is **not** a registered Fabric type and **not** a Unicode codepoint, the node still renders as a styled box with just the label — no icon or type subtitle.

### Generating Diagram SVGs

After adding or updating a `mermaid_diagram` field, you need to generate the corresponding SVG images. Use the **Diagram Generator** page on the website:

1. Start the dev server (or use the deployed site):
   ```bash
   cd src/msfabric_solution_catalog_web
   npm run dev
   ```
2. Navigate to [`/tools/diagram-generator`](http://localhost:8080/tools/diagram-generator)
3. Paste your Mermaid syntax and enter the catalog's `logical_id` as the slug
4. Click **Download Light + Dark SVGs** — this downloads `{slug}_light.svg` and `{slug}_dark.svg`
5. Place both files in `assets/images/diagrams/` at the repository root
6. Commit the SVGs along with your YAML changes

> **Note:** The diagram generator page is not linked from the site navigation — it is a contributor tool only.

> **Important:** CI does not generate diagram SVGs. If you add a `mermaid_diagram` field without committing the corresponding SVGs, the diagram will appear as a broken image on the website.


