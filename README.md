# BAMDataStore

This is the main repository of the BAM Data Store project. This is both a Python package and a web connecting the different resources for the Data Store.


<!--
## Getting started

 Add here installation instructions once the package is deployed -->

## Development

If you want to develop locally this package, clone the project and enter in the workspace folder:
```sh
git clone https://git.bam.de/bam-data-store/bam-data-store.git
cd bam-data-store
```

Create a virtual environment (you can use Python>3.9) in your workspace:
```sh
python3 -m venv .venv
source .venv/bin/activate
```

Run the following script:
```sh
./scripts/install_python_dependencies
```


### Run the tests

You can locally run the tests by doing:
```sh
python -m pytest -sv tests
```

where the `-s` and `-v` options toggle the output verbosity.

You can also generate a local coverage report:
```sh
python -m pytest --cov=src tests
```

### Run auto-formatting and linting

We use [Ruff](https://docs.astral.sh/ruff/) for formatting and linting the code following the rules specified in the `pyproject.toml`. You can run locally:
```sh
ruff check .
```

This will produce an output with the specific issues found. In order to auto-fix them, run:
```sh
ruff format . --check
```

If some issues are not possible to fix automatically, you will need to visit the file and fix them by hand.

### Run the local website

You need to have _Node.js_ installed in your machine. Go to the [installation website](https://nodejs.org/en/download/package-manager) and follow the instructions there to install Node.

Then, go to the `gui/` directory and install the dependencies:
```sh
npm install
```

Run the server:
```sh
npm run dev
```

This will produce an output that looks like:
```sh
> gui@0.1.0 dev
> next dev

   ▲ Next.js 15.0.3
   - Local:        http://localhost:3000

 ✓ Starting...
 ✓ Ready in 2.5s
```

Simply click on `http://localhost:3000` to launch the local server and develop the web.

<!-- ### Debugging

For interactive debugging of the tests, use `pytest` with the `--pdb` flag. We recommend using an IDE for debugging, e.g., _VSCode_. If that is the case, add the following snippet to your `.vscode/launch.json`:
```json
{
  "configurations": [
      {
        "name": "<descriptive tag>",
        "type": "debugpy",
        "request": "launch",
        "cwd": "${workspaceFolder}",
        "program": "${workspaceFolder}/.pyenv/bin/pytest",
        "justMyCode": true,
        "env": {
            "_PYTEST_RAISE": "1"
        },
        "args": [
            "-sv",
            "--pdb",
            "<path-to-plugin-tests>",
        ]
    }
  ]
}
```

where `<path-to-plugin-tests>` must be changed to the local path to the test module to be debugged.

The settings configuration file `.vscode/settings.json` automatically applies the linting and formatting upon saving the modified file. -->

### Documentation on Github pages

To view the documentation locally, make sure to have installed the extra packages (this is part of the `scripts/install_python_dependencies.sh`, so if you ran this script before, you don't need to do it again now):
```sh
uv pip install -e '[docu]'
```

The first time, build the server:
```sh
mkdocs build
```

Run the documentation server:
```sh
mkdocs serve
```

The output looks like:
```sh
INFO    -  Building documentation...
INFO    -  Cleaning site directory
INFO    -  [14:07:47] Watching paths for changes: 'docs', 'mkdocs.yml'
INFO    -  [14:07:47] Serving on http://127.0.0.1:8000/
```

Simply click on `http://127.0.0.1:8000/`. The changes in the `md` files of the documentation are inmediately reflected when the files are saved (the local web will automatically refresh).

## Main contributors

| Name | E-mail     | Role |
|------|------------|--------|
| Dr. Angela Ariza | [angela.ariza@bam.de](mailto:angela.ariza@bam.de) | Outreach and Training |
| Caroline Demidova | [caroline.demidova@bam.de](mailto:caroline.demidova@bam.de) | Outreach and Training |
| Daniel Kosztyla | [daniel.kosztyla@bam.de](mailto:daniel.kosztyla@bam.de) | IT |
| Carlos Madariaga | [carlos.madariaga@bam.de](mailto:carlos.madariaga@bam.de) | Software Developer |
| Kristina Meindl | [kristina.meindl@bam.de](mailto:kristina.meindl@bam.de) | Project Manager |
| Dr. Jose M. Pizarro | [jose.pizarro-blanco@bam.de](mailto:jose.pizarro-blanco@bam.de) | Data Management |
| Jörg Rädler | [joerg.raedler@bam.de](mailto:joerg.raedler@bam.de) | IT |
