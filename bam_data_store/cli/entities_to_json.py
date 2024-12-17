import inspect
import os
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from structlog._config import BoundLoggerLazyProxy

import click

from bam_data_store.utils import delete_and_create_dir, import_module


def entities_to_json(
    module_path: str, export_dir: str, logger: 'BoundLoggerLazyProxy'
) -> None:
    """
    Export entities to JSON files. The Python modules are imported using the function `import_module`,
    and their contents are inspected (using `inspect`) to find the classes in the datamodel containing
    `defs` and with a `to_json` method defined.

    Args:
        module_path (str): Path to the Python module file.
        export_dir (str): Path to the directory where the JSON files will be saved.
        logger (BoundLoggerLazyProxy): The logger to log messages.
    """
    module = import_module(module_path=module_path)
    module_export_dir = os.path.join(
        export_dir, os.path.basename(module_path).replace('.py', '')
    )
    delete_and_create_dir(directory_path=module_export_dir, logger=logger)
    for name, obj in inspect.getmembers(module, inspect.isclass):
        # Ensure the class has the `to_json` method
        if not hasattr(obj, 'defs') or not callable(getattr(obj, 'to_json')):
            continue

        try:
            # Instantiate the class and call the method
            json_data = obj().to_json(indent=2)

            # Write JSON data to file
            output_file = os.path.join(module_export_dir, f'{obj.defs.code}.json')
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(json_data)

            click.echo(f'Saved JSON for class {name} to {output_file}')
        except Exception as err:
            click.echo(f'Failed to process class {name} in {module_path}: {err}')
