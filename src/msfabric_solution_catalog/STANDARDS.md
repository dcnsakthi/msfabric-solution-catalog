# Core Standards
- catalogs are mature and tested Fabric accelerators, demos, and tutorials.
- With limited exception, catalogs must be complete solutions as deployed via `catalog.install(<catalog-id>)`. Unless currently impossible to completely automate, the entirety of the solution must be configured through the installation process.
    - Data must also be self-contained as part of what the catalog deploys. Consider triggering data generators like `LakeGen` or public data sources.
    - catalogs can upload small files (or folders) from the source repository to a Lakehouse's Files area after deployment. Configure this via the optional `files_source_path`, `files_destination_lakehouse`, and `files_destination_path` fields in the YAML `source` block. Keep uploaded data small — the source repository should remain lightweight.
    - catalog will support a pre/post deployment script concept, this feature is not yet supported #20.
- catalogs do not automatically trigger Fabric Items (i.e. Pipelines, Notebooks, etc.) to run after installation. A Notebook with robust markdown instructions should be included in the installation that will reference any user actions.
    - Where Notebooks reference to do something with another Fabric Item, dynamic links should be used (use param replacement to generate dynamic link)

## Choosing a GitHub repo for your catalog
The source repository should be lightweight to avoid cloning a single branch taking more than a second or two.
- Remote catalogs must have a `repo_ref` that is a commit ID or ideally a tag version number (i.e. `v1.0.0`). Branch references will not be allowed so that code drift doesn't occur without a PR to the msfabric-solution-catalog repo to note the changes and allow for testing of the source code before the library distribution is updated.
> Complex catalogs should be self-contained in an isolated repository. Small catalogs may be grouped into shared respositories, provided that the overall Project is small in size and has clear governance.

# catalog Entry Points
The `entry_point` of the catalog is where "Get Started" button links to. This is the starting place for the user to experience the Jumsptart. It must be extremely obvious what the user needs to do, and therefore must be something supporting rich documentation and text, such as a notebook or a documentation web page. For example, if the `entry_point` is a Notebook, it should:
- reference the name of the catalog
- reference the objectives of the catalog
- reference any actions the user must take (if the `entry_point` is a data emulator notebook, make it explicitly clear what the notebook does and that the user needs to run it!)
- reference what the user should do next (does the user go to another Fabric Item?)
- look professional!

## Self-Documenting Source Code
Source code should be self-documenting where possible.
- Notebooks should self contain robust instructions via markdown. Do not reference instructions in Word documents OR in markdown files from source repositories.

## catalog Ownership
- Each catalog will be owned by a mail enabled security group (i.e. `fabriccatalog.spark-structured-streaming@microsoft.com`).That group will have at least two owners.
- The group will be automatically notificed if the nightly catalog CI build fails. The owners are expected to remediate any code changes ASAP as catalogs with failing test cases (deployment or post-deployment solution validation) will automatically be excluded from what each new release published to PyPi to limit the possibility of users executing catalogs that are known to be in a failing state.

## Unlisted vs. Listed catalogs
catalogs with the `include_in_listing: False` config won't show up when listing catalogs. These are _unlisted_, not meant for general discoverability. These catalogs will adhere to the same rigor as listed catalogs.

