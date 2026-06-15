# Getting Started with Fabric catalog

This tutorial walks you through the prerequisites for deploying and running a catalog in Microsoft Fabric. By the end, you'll have a workspace ready, a notebook open, and the `msfabric-solution-catalog` library installed.

## Prerequisites

Before you begin, make sure you have:

- Admin, Member, or Contributor permissions on an existing workspace, or the ability to create a new workspace
- A Fabric-enabled capacity (P or F) or Fabric trial capacity assigned to the workspace

## Step 1: Select a Fabric Workspace

A workspace is the container for all Fabric items. Each catalog will deploys into a single workspace. If a `workspace_id` is not specified at runtime, it will deploy into the current workspace.

_If you do not have an existing workspace:_
1. Go to [Microsoft Fabric](https://app.fabric.microsoft.com/)
2. In the left navigation pane, select **Workspaces**
3. Select **+ New workspace**
4. Enter a name for your workspace (e.g., `my-catalog-workspace`)
5. Expand **Advanced** and make sure your workspace is assigned to a Fabric-enabled capacity
6. Select **Apply**

> **Tip:** Multiple catalogs can be deployed in a single workspace. If items with the same name exist across catalogs (or items already existing in your workspace), the installer will detect the conflict and let you choose how to resolve it:
>
> - **Use a dedicated workspace** — deploy each catalog in its own workspace to avoid conflicts entirely
> - **Automatic prefix** — let the installer automatically prefix items to avoid name collisions
> - **Custom prefix** — set your own prefix, e.g. `catalog.install("demo", item_prefix="demo_")`
> - **Upgrade** — overwrite existing items with conflicting names
>
> See [Handling Name Conflicts](https://github.com/dcnsakthi/msfabric-solution-catalog/tree/main/src/msfabric_solution_catalog#handling-name-conflicts) for more details.

## Step 2: Create a Notebook

Notebooks are the primary interface for installing and interacting with catalogs. You'll use a notebook to run the installation commands and follow along with the catalog's guided experience.

1. Inside your workspace, select **+ New item**
2. Choose **Notebook**
3. Give the notebook a name (e.g., `catalog-setup`) and click **Create**
4. The notebook will open in the Fabric notebook editor

## Step 3: Install the msfabric-solution-catalog Library

The `msfabric-solution-catalog` Python library lets you browse, install, and manage catalogs directly from a Fabric notebook.

In the first cell of your notebook, run the following command to install the library:

```python
%pip install -q msfabric-solution-catalog
```

The `-q` flag runs the installation quietly, reducing output noise. After the cell finishes executing, the library is ready to use.

## Step 4: Browse Available catalogs

Once the library is installed, you can explore the catalog of available catalogs:

```python
import msfabric_solution_catalog as catalog

# List all available catalogs
catalog.list()
```

This displays an interactive catalog of all available catalogs with descriptions, tags, and deployment details.

## Step 5: Install a catalog

Each catalog in the catalog includes a ready-to-use install command — just click the copy button and paste it into a notebook cell. For example:

```python
# Install a catalog by its logical ID
catalog.install("healthcare-billing-system")
```

The installer will:

1. Deploy Fabric items (notebooks, lakehouses, pipelines, etc.) into your current workspace
1. Display progress and log messages
1. Provide a summary of what was installed

> **Note:** Each catalog provides an estimated install time. Deployment duration varies based on the number of items, item types, and their sizes.

## Next Steps

After installing a catalog, follow the "Get Started" link provided when the catalog installation is complete. This link will take you either to a Notebook or catalog documentation page with step-by-step guidance on how to run and explore the scenario.


