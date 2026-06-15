<p align="center">
  <img src="https://github.com/dcnsakthi/msfabric-solution-catalog/raw/main/src/msfabric_solution_catalog_web/public/dark-logo-right.svg" alt="Solution catalog logo" width="720">
  <p align="center">
    Ready-to-run accelerators, demos, and tutorials for <a href="https://www.microsoft.com/en-us/microsoft-fabric">Microsoft Fabric</a> — automated, high-quality, and open-source.
    <br />
    <br />
    <a href="https://pypi.org/project/msfabric-solution-catalog/">PyPI Package</a>
    ·
    <a href="https://dcnsakthi.github.io/msfabric-solution-catalog/catalog">Browse catalogs</a>
    ·
    <a href="CONTRIBUTING.md">Contributing</a>
  </p>
</p>

## What is a catalog?

A **catalog** is a curated, tested Microsoft Fabric solution — data, notebooks, pipelines, reports, and supporting assets — that you can deploy end-to-end with a single call. Each catalog is self-contained: data is bundled or generated for you, and post-install notebooks guide any manual configuration.

## Projects

| Project                                               | Description                                                                                                                                               |
| ----------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [**msfabric-solution-catalog**](src/msfabric_solution_catalog/)         | Core Python library — discover, install, and manage catalogs in your Fabric workspace. Published to [PyPI](https://pypi.org/project/msfabric-solution-catalog/). |
| [**msfabric-solution-catalog-web**](src/msfabric_solution_catalog_web/) | Website for browsing catalogs — hosted at [msfabric-solution-catalog | msfabric-solution-catalog catalog](https://dcnsakthi.github.io/msfabric-solution-catalog/catalog).                                     |

## Quick Start

```bash
pip install msfabric-solution-catalog
```

```python
import msfabric_solution_catalog as catalog

# Browse the catalog
catalog.list()

# Deploy to your workspace
catalog.install("spark-structured-streaming")
```

See the [msfabric-solution-catalog README](src/msfabric_solution_catalog/README.md) for full usage, conflict handling, and API details.

## Contributing

Please follow the contribution process in [CONTRIBUTING.md](CONTRIBUTING.md) and the coding expectations in [STANDARDS.md](STANDARDS.md).

## Learn More

- **Browse catalogs**: https://dcnsakthi.github.io/msfabric-solution-catalog/catalog
- **PyPI**: https://pypi.org/project/msfabric-solution-catalog/
- **fabric-cicd**: https://microsoft.github.io/fabric-cicd/latest/



