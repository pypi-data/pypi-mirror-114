import inspect
import json
import os

import click
import pkg_resources
import toml
from click.exceptions import ClickException
from cmr import render
from cookiecutter import generate
from cookiecutter.exceptions import OutputDirExistsException
from cookiecutter.main import cookiecutter
from cookiecutter.utils import work_in

from connect.cli.core.utils import is_bundle
from connect.cli.plugins.project.constants import (
    CAPABILITY_ALLOWED_STATUSES,
    CAPABILITY_METHOD_MAP,
    PROJECT_EXTENSION_BOILERPLATE_URL,
)
from connect.cli.plugins.project import utils


def bootstrap_extension_project(config, data_dir: str):
    click.secho('Bootstraping extension project...\n', fg='blue')

    utils.purge_cookiecutters_dir()

    index = 1
    answers = {}
    function_list = [
        'general_extension_questions',
        'credentials_questions',
        'asset_process_capabilities',
        'asset_validation_capabilities',
        'tier_config_capabilities',
        'product_capabilities',
    ]

    for question_function in function_list:
        partial = getattr(utils, question_function)(config, index, len(function_list))
        index += 1
        answers.update(partial)

    try:
        if is_bundle():
            method_name = '_run_hook_from_repo_dir'
            setattr(generate, method_name, getattr(utils, method_name))
            with work_in(data_dir):
                utils.pre_gen_cookiecutter_extension_hook(answers)
                project_dir = cookiecutter(
                    PROJECT_EXTENSION_BOILERPLATE_URL,
                    no_input=True,
                    extra_context=answers,
                    output_dir=data_dir,
                )
                utils.post_gen_cookiecutter_extension_hook(answers, project_dir)
        else:
            project_dir = cookiecutter(
                PROJECT_EXTENSION_BOILERPLATE_URL,
                no_input=True,
                extra_context=answers,
                output_dir=data_dir,
            )
        click.secho(f'\nExtension Project location: {project_dir}\n', fg='blue')
        click.echo(render(open(f'{project_dir}/HOWTO.md', 'r').read()))
    except OutputDirExistsException as error:
        project_path = str(error).split('"')[1]
        raise ClickException(
            f'\nThe directory "{project_path}" already exists, '
            '\nif you would like to use that name, please delete '
            'the directory or use another location.',
        )


def validate_extension_project(project_dir: str):
    click.secho(f'Validating project {project_dir}...\n', fg='blue')

    if is_bundle():
        raise ClickException(
            '\nThis project can not be validated since you are running outside a development environment.'
            '\nCurrently in order to validate the project is required that you run the CloudBlue Connect CLI'
            '\ntool in the same environment where the extension runs.\n'
            '\nIn the use case that you are developing using the standard dockerized environment, we suggest'
            '\nto install the ´connect-cli´ tool inside it to validate the project, this can be accomplished'
            '\nvia starting your extension using the bash option, as example'
            '\n\n$ docker compose run my_extension_bash\n'
            '\nOnce you get the bash, you can install the CloudBlue Connect CLI tool inside it using pip:'
            '\n\n$ pip install connect-cli\n'
            '\nonce done you can run again.',
        )

    extension_dict = _project_descriptor_validations(project_dir)
    _entrypoint_validations(project_dir, extension_dict)

    click.secho(f'Extension Project {project_dir} has been successfully validated.', fg='green')


def _project_descriptor_validations(project_dir):
    descriptor_file = os.path.join(project_dir, 'pyproject.toml')
    if not os.path.isfile(descriptor_file):
        raise ClickException(
            f'The directory `{project_dir}` does not look like an extension project directory, '
            'the mandatory `pyproject.toml` project descriptor file is not present.',
        )
    try:
        data = toml.load(descriptor_file)
    except toml.TomlDecodeError:
        raise ClickException(
            'The extension project descriptor file `pyproject.toml` is not valid.',
        )

    extension_dict = data['tool']['poetry']['plugins']['connect.eaas.ext']
    if not isinstance(extension_dict, dict):
        raise ClickException(
            'The extension definition on [tool.poetry.plugins."connect.eaas.ext"] `pyproject.toml` section '
            'is not well configured. It should be as following: "extension" = "your_package.extension:YourExtension"',
        )
    if 'extension' not in extension_dict.keys():
        raise ClickException(
            'The extension definition on [tool.poetry.plugins."connect.eaas.ext"] `pyproject.toml` section '
            'does not have "extension" defined. Reminder: "extension" = "your_package.extension:YourExtension"',
        )
    return extension_dict


def _entrypoint_validations(project_dir, extension_dict):
    package_name = extension_dict['extension'].rsplit('.', 1)[0]
    descriptor_file = os.path.join(f'{project_dir}/{package_name}', 'extension.json')
    if sum(1 for _ in pkg_resources.iter_entry_points('connect.eaas.ext', 'extension')) > 1:
        raise ClickException('\nOnly one extension can be loaded at a time!!!')

    ext_class = next(pkg_resources.iter_entry_points('connect.eaas.ext', 'extension'), None)
    if not ext_class:
        raise ClickException('\nThe extension could not be loaded, Did you execute `poetry install`?')

    CustomExtension = ext_class.load()
    if not inspect.isclass(CustomExtension):
        raise ClickException(f'\nThe extension class {CustomExtension} does not seem a class, please check it')

    all_methods = CustomExtension.__dict__
    methods = [method for method in all_methods.keys() if method in CAPABILITY_METHOD_MAP.values()]

    try:
        ext_descriptor = json.load(open(descriptor_file, 'r'))
    except json.JSONDecodeError:
        raise ClickException(
            '\nThe extension descriptor file `extension.json` could not be loaded.',
        )

    capabilities = ext_descriptor['capabilities']

    errors = _have_capabilities_proper_stats(capabilities)
    if errors:
        raise ClickException(f'Capability errors: {errors}')

    errors = _have_methods_proper_capabilities(methods, capabilities)
    if errors:
        raise ClickException(f'Capability-Method errors: {errors}')

    _have_methods_proper_type(CustomExtension, capabilities)


def _have_methods_proper_type(cls, capabilities):
    guess_async = [
        inspect.iscoroutinefunction(getattr(cls, CAPABILITY_METHOD_MAP.get(name)))
        for name in capabilities.keys()
    ]
    if all(guess_async):
        return
    if not any(guess_async):
        return

    raise ClickException('An Extension class can only have sync or async methods not a mix of both.')


def _have_capabilities_proper_stats(capabilities):
    errors = []
    for capability, stats in capabilities.items():
        if capability == 'product_action_execution' or capability == 'product_custom_event_processing':
            if isinstance(stats, list) and len(stats) != 0:
                errors.append(f'Capability `{capability}` must not have status.')
            continue
        if not stats:
            errors.append(f'Capability `{capability}` must have at least one allowed status.')
        for stat in stats:
            if stat not in CAPABILITY_ALLOWED_STATUSES:
                errors.append(f'Status `{stat}` on capability `{capability}` is not allowed.')
    return errors


def _have_methods_proper_capabilities(methods, capabilities):
    errors = []
    for capability in capabilities.keys():
        if CAPABILITY_METHOD_MAP.get(capability) not in methods:
            errors.append(
                f'Capability ´{capability}´ does not have '
                f'corresponding ´{CAPABILITY_METHOD_MAP.get(capability)}´ method',
            )
    return errors
