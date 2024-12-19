import json
import os
import shutil

import pytest

from bam_masterdata.cli.entities_to_json import entities_to_json
from bam_masterdata.logger import logger


@pytest.mark.parametrize(
    'module_name',
    [
        ('collection_types'),
        # ('dataset_types', False),  # ! this module does not have classes yet
        ('object_types'),
        ('property_types'),
        ('vocabulary_types'),
    ],
)
def test_entities_to_json(module_name: str):
    """Test the `entities_to_json` function."""
    export_dir = './tests/data/tmp/'
    module_path = os.path.join('./bam_masterdata/datamodel', f'{module_name}.py')

    entities_to_json(module_path=module_path, export_dir=export_dir, logger=logger)

    module_export_dir = os.path.join(export_dir, module_name)
    assert os.path.exists(export_dir)
    assert len(os.listdir(module_export_dir)) > 0
    assert ['.json' in f for f in os.listdir(module_export_dir)]

    for file in os.listdir(module_export_dir):
        with open(os.path.join(module_export_dir, file)) as f:
            data = json.load(f)
            # making sure the data stored in json files is correct
            if module_name == 'property_types':
                assert data['code'] == file.replace('.json', '')
            else:
                assert data['defs']['code'] == file.replace('.json', '')

    shutil.rmtree(export_dir)  # ! careful with this line
