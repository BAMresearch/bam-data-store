import inspect
import os
import shutil

import pytest

from bam_data_store.logger import log_storage, logger
from bam_data_store.utils import (
    delete_and_create_dir,
    import_module,
    listdir_py_modules,
)


@pytest.fixture(autouse=True)
def clear_log_storage():
    """Fixture to clear the log storage before each test."""
    log_storage.clear()


@pytest.mark.parametrize(
    'directory_path, dir_exists',
    [
        # `directory_path` is empty
        ('', False),
        # `directory_path` does not exist and it is created
        ('tests/data/tmp/', True),
    ],
)
def test_delete_and_create_dir(directory_path: str, dir_exists: bool):
    """Tests the `delete_and_delete_dir` function."""
    delete_and_create_dir(directory_path=directory_path, logger=logger)
    assert dir_exists == os.path.exists(directory_path)
    if dir_exists:
        shutil.rmtree(directory_path)  # ! careful with this line
    else:
        assert len(log_storage) == 1
        assert log_storage[0]['level'] == 'warning'
        assert 'directory_path' in log_storage[0]['event']


@pytest.mark.parametrize(
    'directory_path, listdir, log_message, log_message_level',
    [
        # `directory_path` is empty
        (
            '',
            [],
            'The `directory_path` is empty. Please, provide a proper input to the function.',
            'warning',
        ),
        # No Python files found in the directory
        ('./tests/data', [], 'No Python files found in the directory.', 'info'),
        # Python files found in the directory
        (
            './tests',
            [
                './tests/conftest.py',
                './tests/metadata/test_entities.py',
                './tests/metadata/test_definitions.py',
                './tests/utils/test_utils.py',
            ],
            None,
            None,
        ),
    ],
)
def test_listdir_py_modules(
    directory_path: str, listdir: list[str], log_message: str, log_message_level: str
):
    """Tests the `listdir_py_modules` function."""
    result = listdir_py_modules(directory_path=directory_path, logger=logger)
    if not listdir:
        assert log_storage[0]['event'] == log_message
        assert log_storage[0]['level'] == log_message_level
    assert result == listdir


def test_import_module():
    """Tests the `import_module` function."""
    # testing only the possitive results
    module = import_module('./bam_data_store/utils/utils.py')
    assert [f[0] for f in inspect.getmembers(module, inspect.ismodule)] == [
        'glob',
        'importlib',
        'os',
        'shutil',
    ]
    assert [f[0] for f in inspect.getmembers(module, inspect.isclass)] == []
    assert [f[0] for f in inspect.getmembers(module, inspect.isclass)] == [
        'delete_and_create_dir',
        'import_module',
        'listdir_py_modules',
    ]
