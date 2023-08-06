import pytest
from pathlib import Path


install_folder = Path(__file__).parent.resolve()
test_folder = install_folder / 'tests'
print(test_folder)
pytest.main([f'--rootdir={install_folder}',f'--pyargs data_steps'])
