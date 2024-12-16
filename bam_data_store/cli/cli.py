import importlib.util
import inspect
import os
from typing import Optional

import click

from bam_data_store.logger import logger
from bam_data_store.utils import delete_and_create_dir, listdir_py_modules


def import_module(module_path: str):
    """
    Dynamically imports a module from the given file path.

    Args:
        module_path (str): Path to the Python module file.

    Returns:
        module: Imported module object.
    """
    module_name = os.path.splitext(os.path.basename(module_path))[0]
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def entities_to_json(module_path: str, export_dir: str) -> None:
    module = import_module(module_path=module_path)
    for name, obj in inspect.getmembers(module, inspect.isclass):
        # Ensure the class has the `to_json` method
        if not hasattr(obj, 'defs') or not callable(getattr(obj, 'to_json')):
            continue

        try:
            # Instantiate the class and call the method
            json_data = obj().to_json(indent=2)

            # Write JSON data to file
            output_file = os.path.join(export_dir, f'{obj.defs.code}.json')
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(json_data)
            print(f'Saved JSON for class {name} to {output_file}')
        except Exception as err:
            print(f'Failed to process class {name} in {module_path}: {err}')


@click.group(help='Entry point to run `bam_data_store` CLI commands.')
def cli():
    pass


@cli.command(
    help='Export entities to JSON files to the `./bam_data_store/datamodel/artifacts/` subfolder.'
)
def export_entities_to_json():
    datamodel_dir = os.path.join('.', 'bam_data_store', 'datamodel')
    export_dir = os.path.join('.', 'bam_data_store', 'datamodel', 'artifacts')

    # Delete and create the export directory
    delete_and_create_dir(directory_path=export_dir, logger=logger)

    # Get the Python modules to process the datamodel
    py_modules = listdir_py_modules(directory_path=datamodel_dir)

    # Process each module
    for module_path in py_modules:
        entities_to_json(module_path=module_path, export_dir=export_dir)

    click.echo(f'All entity artifacts have been generated and saved to {export_dir}')


if __name__ == '__main__':
    cli()
