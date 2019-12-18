import pytest
import os
from glob import glob
from shutil import rmtree


@pytest.fixture()
def remove_generated_reports_in_root():
    yield
    path = os.getcwd()
    pattern = os.path.join(
        path, "graph-of-xccdf_org.ssgproject.content_rule_package_abrt_removed*")
    for item in glob(pattern):
        if not os.path.isdir(item):
            continue
        rmtree(item)