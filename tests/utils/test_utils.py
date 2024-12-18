import inspect
import os
import shutil

import pytest

from bam_masterdata.logger import logger
from bam_masterdata.utils import (
    delete_and_create_dir,
    import_module,
    listdir_py_modules,
)


@pytest.mark.parametrize(
    'directory_path, dir_exists',
    [
        # `directory_path` is empty
        ('', False),
        # `directory_path` does not exist and it is created
        ('tests/data/tmp/', True),
    ],
)
def test_delete_and_create_dir(
    cleared_log_storage: list, directory_path: str, dir_exists: bool
):
    """Tests the `delete_and_delete_dir` function."""
    delete_and_create_dir(directory_path=directory_path, logger=logger)
    assert dir_exists == os.path.exists(directory_path)
    if dir_exists:
        shutil.rmtree(directory_path)  # ! careful with this line
    else:
        assert len(cleared_log_storage) == 1
        assert cleared_log_storage[0]['level'] == 'warning'
        assert 'directory_path' in cleared_log_storage[0]['event']


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
            './tests/utils',
            [
                './tests/utils/test_utils.py',
            ],
            None,
            None,
        ),
    ],
)
def test_listdir_py_modules(
    cleared_log_storage: list,
    directory_path: str,
    listdir: list[str],
    log_message: str,
    log_message_level: str,
):
    """Tests the `listdir_py_modules` function."""
    result = listdir_py_modules(directory_path=directory_path, logger=logger)
    if not listdir:
        assert cleared_log_storage[0]['event'] == log_message
        assert cleared_log_storage[0]['level'] == log_message_level
    # when testing locally and with Github actions the order of the files is different --> `result` is sorted, so we also sort `listdir`
    assert result == sorted(listdir)


@pytest.mark.skip(
    reason='Very annoying to test this function, as any module we can use to be tested will change a lot in the future.'
)
def test_import_module():
    """Tests the `import_module` function."""
    # testing only the possitive results
    module = import_module('./bam_data_store/utils/utils.py')
    assert [f[0] for f in inspect.getmembers(module, inspect.ismodule)] == [
        'glob',
        'importlib',
        'os',
        'shutil',
        'sys',
    ]
    assert [f[0] for f in inspect.getmembers(module, inspect.isclass)] == []
    assert [f[0] for f in inspect.getmembers(module, inspect.isfunction)] == [
        'delete_and_create_dir',
        'import_module',
        'listdir_py_modules',
    ]
