import os

import click

from bam_data_store.cli.entities_to_json import entities_to_json
from bam_data_store.logger import logger
from bam_data_store.utils import delete_and_create_dir, listdir_py_modules


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
    py_modules = listdir_py_modules(directory_path=datamodel_dir, logger=logger)

    # Process each module
    for module_path in py_modules:
        entities_to_json(module_path=module_path, export_dir=export_dir)

    click.echo(f'All entity artifacts have been generated and saved to {export_dir}')


if __name__ == '__main__':
    cli()
