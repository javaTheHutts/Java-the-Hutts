from pybuilder.core import init, use_plugin

use_plugin('python.core')
use_plugin('pypi:pybuilder_pytest')
use_plugin('python.integrationtest')
use_plugin('python.pylint')
use_plugin('python.coverage')
use_plugin('python.install_dependencies')
use_plugin('python.distutils')

default_task = "publish"

@init
def init(project):
    # directory with pytest modules
    project.set_property("dir_source_pytest_python", "src/unittest/python")
    # filename pattern to use for unit testing files
    project.set_property("unittest_module_glob", "test_*")
    # extra arguments which will be passed to pytest
    project.get_property("pytest_extra_args").append("-x")
    # filename pattern to use for integration testing files
    project.set_property("integrationtest_file_glob", "itest_*")

