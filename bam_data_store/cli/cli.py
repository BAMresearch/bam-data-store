import os

import click
from openpyxl import Workbook

from bam_data_store.cli.entities_to_excel import entities_to_excel
from bam_data_store.cli.entities_to_json import entities_to_json
from bam_data_store.logger import logger
from bam_data_store.utils import (
    delete_and_create_dir,
    import_module,
    listdir_py_modules,
)


@click.group(help='Entry point to run `bam_data_store` CLI commands.')
def cli():
    pass


@cli.command(help='Export entities to JSON files to the `./artifacts/` folder.')
def export_entities_to_json():
    # Get the directories from the Python modules and the export directory for the static artifacts
    datamodel_dir = os.path.join('.', 'bam_data_store', 'datamodel')
    export_dir = os.path.join('.', 'artifacts')

    # Delete and create the export directory
    delete_and_create_dir(directory_path=export_dir, logger=logger)

    # Get the Python modules to process the datamodel
    py_modules = listdir_py_modules(directory_path=datamodel_dir, logger=logger)

    # Process each module using the `to_json` method of each entity
    for module_path in py_modules:
        entities_to_json(module_path=module_path, export_dir=export_dir, logger=logger)

    click.echo(f'All entity artifacts have been generated and saved to {export_dir}')


@cli.command(
    help="""
    Export entities to an Excel file in the path `./artifacts/masterdata.xlsx`.
    """,
)
def export_entities_to_excel():
    # Get the Python modules to process the datamodel
    datamodel_dir = os.path.join('.', 'bam_data_store', 'datamodel')
    py_modules = listdir_py_modules(directory_path=datamodel_dir, logger=logger)

    # Load the definitions module classes
    definitions_module = import_module(
        module_path='./bam_data_store/metadata/definitions.py'
    )

    # Process the modules and save the entities to the openBIS masterdata Excel file
    masterdata_file = os.path.join('.', 'artifacts', 'masterdata.xlsx')
    wb = Workbook()
    for i, module_path in enumerate(py_modules):
        if i == 0:
            ws = wb.active
        else:
            ws = wb.create_sheet()
        ws.title = (
            os.path.basename(module_path)
            .capitalize()
            .replace('.py', '')
            .replace('_', ' ')
        )
        entities_to_excel(
            worksheet=ws,
            module_path=module_path,
            definitions_module=definitions_module,
            logger=logger,
        )
    wb.save(masterdata_file)

    click.echo(f'All masterdata have been generated and saved to {masterdata_file}')


if __name__ == '__main__':
    cli()
