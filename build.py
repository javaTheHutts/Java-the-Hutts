from pybuilder.core import after, task, init, use_plugin, depends
from pybuilder.errors import BuildFailedException
from pybuilder.utils import assert_can_execute
from pybuilder.pluginhelper.external_command import ExternalCommandBuilder

use_plugin('python.core')
use_plugin('vcs:git+https://github.com/AlexeySanko/pybuilder_pytest.git', plugin_module_name="pybuilder_pytest")
use_plugin('python.integrationtest')
use_plugin('python.flake8')
use_plugin('python.coverage')
use_plugin('python.install_dependencies')
use_plugin('python.distutils')

default_task = "publish"

@init
def init(project):
    project.plugin_depends_on("flake8", "~=3.2")
    project.depends_on_requirements("requirements.txt")

    # directory with pytest modules
    project.set_property("dir_source_pytest_python", "src/unittest/python")
    # filename pattern to use for unit testing files
    project.set_property("unittest_module_glob", "test_*")
    # extra arguments which will be passed to pytest
    project.set_property_if_unset("pytest_extra_args", [])
    project.get_property("pytest_extra_args").append("-x")
    # filename pattern to use for integration testing files
    project.set_property("integrationtest_file_glob", "itest_*")
    # don't break the build if the coverage is below threshold
    project.set_property("coverage_break_build", False)
    # display verbose linting output
    project.set_property("flake8_verbose_output", True)
    project.set_property("flake8_break_build", True)
    project.set_property_if_unset("flake8_max_line_length", 120)
    project.set_property_if_unset("flake8_include_patterns", None)
    project.set_property_if_unset("flake8_exclude_patterns", None)
    project.set_property_if_unset("flake8_include_test_sources", False)
    project.set_property_if_unset("flake8_include_scripts", False)
    project.set_property_if_unset("flake8_max_complexity", None)

@after("prepare")
def assert_flake8_is_executable(logger):
    """ Asserts that the flake8 script is executable. """
    logger.debug("Checking if flake8 is executable.")

    assert_can_execute(command_and_arguments=["flake8", "--version"],
                       prerequisite="flake8",
                       caller="plugin python.flake8")

@task("full", description="Includes all of the data files in the installation process.")
@after("prepare")
def full_setup(project, logger):
    # include the training data in the correct package
    logger.info("Including the data files in the installation...")
    img_pre_trained_data_path = "lib/python3.5/site-packages/hutts_verification/image_preprocessing/trained_data/"
    img_pre_templates_path = "lib/python3.5/site-packages/hutts_verification/image_preprocessing/templates/"
    project.install_file(img_pre_trained_data_path, "hutts_verification/image_preprocessing/trained_data/dlib_face_recognition_resnet_model_v1.dat")
    project.install_file(img_pre_trained_data_path, "hutts_verification/image_preprocessing/trained_data/shape_predictor_face_landmarks.dat")
    project.install_file(img_pre_templates_path, "hutts_verification/image_preprocessing/templates/pp2.jpg")
    project.install_file(img_pre_templates_path, "hutts_verification/image_preprocessing/templates/temp_flag.jpg")
    project.install_file(img_pre_templates_path, "hutts_verification/image_preprocessing/templates/wap.jpg")

@task
@depends("prepare")
def analyze(project, logger):
    """ Applies the flake8 script to the sources of the given project. """
    logger.info("Executing flake8 on project sources.")

    command = ExternalCommandBuilder('flake8', project)
    command.use_argument('--ignore={0}').formatted_with_truthy_property('flake8_ignore')
    command.use_argument('--max-line-length={0}').formatted_with_property('flake8_max_line_length')
    command.use_argument('--filename={0}').formatted_with_truthy_property('flake8_include_patterns')
    command.use_argument('--exclude={0}').formatted_with_truthy_property('flake8_exclude_patterns')
    command.use_argument('--max-complexity={0}').formatted_with_truthy_property('flake8_max_complexity')

    include_test_sources = project.get_property("flake8_include_test_sources")
    include_scripts = project.get_property("flake8_include_scripts")

    result = command.run_on_production_source_files(logger,
                                                    include_test_sources=include_test_sources,
                                                    include_scripts=include_scripts,
                                                    include_dirs_only=True)

    count_of_warnings = len(result.report_lines)
    count_of_errors = len(result.error_report_lines)

    if count_of_errors > 0:
        logger.error('Errors while running flake8, see {0}'.format(result.error_report_file))

    if count_of_warnings > 0:
        if project.get_property("flake8_break_build"):
            error_message = "flake8 found {0} warning(s)".format(count_of_warnings)
            raise BuildFailedException(error_message)
        else:
            logger.warn("flake8 found %d warning(s).", count_of_warnings)
