# Requirements
- this will be similar to the dbdemos python library. it renders HTML in the Notebook cell output to browse installable solutions.
    - see this local project for an example: C:\Users\milescole\source\dbdemos\fabric_demos
- I want it to have a UI theme that is the same as Arc catalog: https://catalog.azure.com/ see the grid of options after "Explore The Arc catalog universe"
    - do NOT just copy the theme from C:\Users\milescole\source\dbdemos\fabric_demos , this was copying Databricks. Use the catalog theme HTML as we are expanding that brand.
- It should default to listing catalogs cateagorized by `solution_tag` from the `registry`.
- It should allow toggling to viewing catalogs by `workload_tag` from the `registry`.
- It should use the `catalog._registry` from the core.py module as data input.
- A NEW catalog is any that has been created in the last 60 days (from the registry `date_added`)
- catalogs should be sorted in the list by NEW first, and then sorted alphabetical by catalog `id`.
- NEW catalogs should show a NEW callout to identify it as such.
- Each catalog box should
    - render an image (`preview_image` from registry), with fallback to generic background.
    - `name` of catalog
    - `description` of catalog
    - code to install `catalog.install(<id>)`. it sould reference the name or alias of the class instance. i.e. if the `from msfabric_solution_catalog import catalog as js` should render as `js.install()`


