import collections
import inspect
import json
import os
import pprint
import sys

import click

from .backuptools import BackupTools


class OrderedGroup(click.Group):
    def __init__(self, name=None, commands=None, **attrs):
        super(OrderedGroup, self).__init__(name, commands, **attrs)
        #: the registered subcommands by their exported names.
        self.commands = commands or collections.OrderedDict()

    def list_commands(self, ctx):
        return self.commands


class RequiredConditionOption(click.Option):
    def __init__(self, *args, **kwargs):
        self.not_required_if = kwargs.pop('not_required_if', None)
        self.required_if = kwargs.pop('required_if', None)
        self.required_if_command = kwargs.pop('required_if_command', None)
        self.not_required_if_command = kwargs.pop(
            'not_required_if_command', None)
        # assert self.not_required_if, "'not_required_if' parameter required"

        if self.required_if:
            kwargs['help'] = (kwargs.get('help', '') +
                              ' [required when have `%s`]' %
                              self.required_if
                              ).strip()

        if self.not_required_if:
            kwargs['help'] = (kwargs.get('help', '') +
                              ' [mutually exclusive with `%s`]' %
                              self.not_required_if
                              ).strip()

        if self.required_if_command:
            cm = self.required_if_command
            command_text = f'command `{cm}`' if cm != '*' else f'any command'
            kwargs['help'] = (kwargs.get('help', '') +
                              ' [required when have %s]' %
                              command_text
                              ).strip()

        if self.not_required_if_command:
            cm = self.not_required_if_command
            command_text = f'command `{cm}`' if cm != '*' else f'any command'
            kwargs['help'] = (kwargs.get('help', '') +
                              ' [mutually exclusive with %s]' %
                              command_text
                              ).strip()

        super(RequiredConditionOption, self).__init__(*args, **kwargs)

    def handle_parse_result(self, ctx, opts, args):
        we_are_present = self.name in opts

        # click.echo(f'{opts=}')
        # click.echo(f'{args=}')

        if self.not_required_if is not None:
            other_present = (self.not_required_if in opts) or (
                self.not_required_if in args)
            if other_present:
                if we_are_present:
                    raise click.UsageError(
                        "Illegal usage: `%s` is mutually exclusive with `%s`" % (
                            self.name, self.not_required_if), ctx)
                else:
                    self.prompt = None

        if self.required_if is not None:
            other_present = (self.required_if in opts) or (
                self.required_if in args)
            if other_present:
                if not we_are_present:
                    raise click.UsageError(
                        "Illegal usage: `%s` is required with `%s`" % (
                            self.name, self.required_if), ctx)

        if self.required_if_command is not None:
            other_present = False

            if self.required_if_command == '*':
                other_present = len(args) > 0
            else:
                other_present = (self.required_if_command in args[:1])

            if other_present:
                if not we_are_present:
                    raise click.UsageError(
                        "Illegal usage: `%s` is required with command `%s`" % (
                            self.name, args[0]), ctx)

        if self.not_required_if_command is not None:
            other_present = False

            if self.not_required_if_command == '*':
                other_present = len(args) > 0
            else:
                other_present = (self.not_required_if_command in args[:1])

            if other_present:
                if we_are_present:
                    raise click.UsageError(
                        "Illegal usage: `%s` is mutually exclusive with `%s`" % (
                            self.name, args[0]), ctx)
                else:
                    self.prompt = None

        return super(RequiredConditionOption, self).handle_parse_result(
            ctx, opts, args)


class RequiredConditionArgument(click.Argument):
    def __init__(self, *args, **kwargs):
        self.not_required_if = kwargs.pop('not_required_if', None)
        self.required_if = kwargs.pop('required_if', None)

        if self.required_if is not None:
            kwargs['required'] = False

        # assert self.not_required_if, "'not_required_if' parameter required"

        # if self.required_if:
        #     kwargs['help'] = (kwargs.get('help', '') +
        #         ' [required when have `%s`]' %
        #         self.required_if
        #     ).strip()

        # if self.not_required_if:
        #     kwargs['help'] = (kwargs.get('help', '') +
        #         ' [mutually exclusive with `%s`]' %
        #         self.not_required_if
        #     ).strip()

        # if self.required_if_command:
        #     cm = self.required_if_command
        #     command_text = f'command `{cm}`' if cm != '*' else  f'any command'
        #     kwargs['help'] = (kwargs.get('help', '') +
        #         ' [required when have %s]' %
        #         command_text
        #     ).strip()

        # if self.not_required_if_command:
        #     cm = self.not_required_if_command
        #     command_text = f'command `{cm}`' if cm != '*' else  f'any command'
        #     kwargs['help'] = (kwargs.get('help', '') +
        #         ' [mutually exclusive with %s]' %
        #         command_text
        #     ).strip()

        super(RequiredConditionArgument, self).__init__(*args, **kwargs)

    def handle_parse_result(self, ctx, opts, args):
        we_are_present = self.name in opts and opts[self.name] is not None

        # click.echo(f'{opts=}')
        # click.echo(f'{args=}')

        if self.not_required_if is not None:
            other_present = (
                self.not_required_if in opts) and opts[self.not_required_if] is not None
            if other_present:
                if we_are_present:
                    click.echo(f'{we_are_present=}')
                    click.echo(f'{other_present=}')
                    raise click.UsageError(
                        "Illegal usage: `%s` is mutually exclusive with `%s`" % (
                            self.get_error_hint(ctx), self.not_required_if), ctx)
                else:
                    self.prompt = None

        if isinstance(self.required_if, str):
            other_present = (
                self.required_if in opts) and opts[self.required_if] is not None
            if other_present:
                if not we_are_present:
                    raise click.UsageError(
                        "Illegal usage: `%s` is required with `%s`" % (
                            self.get_error_hint(ctx), self.required_if), ctx)

        elif callable(self.required_if):
            other_present = self.required_if(ctx, opts, args)
            if other_present:
                if not we_are_present:
                    raise click.UsageError(
                        f"Illegal usage: {self.get_error_hint(ctx)} is required", ctx)

        return super(RequiredConditionArgument, self).handle_parse_result(
            ctx, opts, args)


def echo_progresses():
    click.secho('Progresses:', bold=True, fg="blue")


def echo_title(title: str):
    click.secho(title, bold=True, fg="blue")


def echo_text(text: str, tab=False):
    click.secho(f'{"  " if tab else ""}{text}')


def echo_completed():
    click.secho('Completed!', bold=True, fg="green")


@click.group(invoke_without_command=True, cls=OrderedGroup)
@click.option('-C', '--config', 'config', help="Config path")
@click.option('-R', '--resource', 'resource', cls=RequiredConditionOption, required_if_command="*", help="Resource name")
@click.pass_context
def cli(ctx, config, resource):
    ctx.ensure_object(dict)
    ctx.obj['config'] = config
    ctx.obj['resource'] = resource

    config_content: dict

    config_path = config or os.path.join(
        os.getcwd(), 'backuptools.config.json')

    if not os.path.isfile(config_path):
        raise click.UsageError(f'Config path `{config_path}` not found', ctx)

    with open(config_path) as f:
        config_content = json.load(f)

    ctx.obj['tools'] = BackupTools(config_content)


@cli.command()
@click.argument('version', type=click.STRING, required=False, default=None)
@click.pass_context
def backup(ctx, version):
    '''
        Create version and upload to remote 
    '''
    resource = ctx.obj['resource']
    tools = ctx.obj['tools']

    if version is None:
        version = tools.exec(resource, 'backup')
    else:
        version = tools.exec(resource, 'backup', version)

    click.secho(f'{version} local', bold=True, fg='blue')
    click.secho(f'{version} remote', bold=True, fg='green')


@cli.command()
@click.argument('version', type=click.STRING, required=True)
@click.pass_context
def restore(ctx, version):
    '''
        Download version and extract to resource 
    '''
    resource = ctx.obj['resource']
    tools = ctx.obj['tools']
    tools.exec(resource, 'restore', version)


@cli.command()
@click.option('--local/--remote', default=None)
@click.pass_context
def ls(ctx, local):
    '''
        Show list version 
    '''
    resource = ctx.obj['resource']
    tools = ctx.obj['tools']

    local_versions = tools.exec(
        resource, 'list_local_version') if local is None or local is True else []
    remote_versions = tools.exec(
        resource, 'list_drive_version') if local is None or local is False else []

    versions = [(version, 'local') for version in local_versions] + \
        [(version, 'remote') for version in remote_versions]

    versions.sort(key=lambda item: item[0])

    for version in versions:
        click.secho(f'{version[0]} {version[1]}', bold=True,
                    fg='blue' if version[1] == 'local' else 'green')


@cli.command()
@click.option('--all', 'is_all', is_flag=True, help='Download all vertions')
@click.argument('version', type=click.STRING, cls=RequiredConditionArgument, not_required_if="is_all", required_if=lambda ctx, opts, args: opts.get('is_all') is None)
@click.pass_context
def pull(ctx, is_all, version):
    '''
        Download version from remote to local
    '''
    resource = ctx.obj['resource']
    tools = ctx.obj['tools']

    echo_progresses()

    if is_all:
        echo_text('Download all')

        # MAIN
        downloaded = tools.exec(resource, 'download_all')

        echo_title(
            f'Downloaded: {len(downloaded)} version')
        for version in downloaded:
            echo_text(f'{version} downloaded!')
    else:
        echo_text(f'Download version `{version}`')

        # MAIN
        tools.exec(resource, 'download_version', version)

        echo_title(f'Downloaded: {1} version')
        echo_text(f'{version} downloaded!', tab=True)

    echo_completed()


@cli.command()
@click.option('--all', 'is_all', is_flag=True, help='Upload all vertions')
@click.argument('version', type=click.STRING, cls=RequiredConditionArgument, not_required_if="is_all", required_if=lambda ctx, opts, args: opts.get('is_all') is None)
@click.pass_context
def push(ctx, is_all, version):
    '''
        Upload local version to remote 
    '''

    resource = ctx.obj['resource']
    tools = ctx.obj['tools']

    echo_progresses()

    if is_all:
        echo_text('Upload all')

        uploaded = tools.exec(resource, 'upload_all')

        echo_title(f'Uploaded: {len(uploaded)} version')
        for version in uploaded:
            echo_text(f'{version} uploaded!', tab=True)
    else:
        echo_text(f'Upload version `{version}`')

        tools.exec(resource, 'upload_version', version)

        echo_title(f'Uploaded: {1} version')
        echo_text(f'{version} uploaded!', tab=True)

    echo_completed()


@cli.command()
@click.pass_context
def sync(ctx):
    '''
        Sync local version and remote version 
    '''
    resource = ctx.obj['resource']
    tools: BackupTools = ctx.obj['tools']

    echo_progresses()

    echo_text('Sync')

    uploaded, downloaded = tools.exec(resource, 'sync')

    echo_title(f'Uploaded: {len(uploaded)} version')
    for version in uploaded:
        echo_text(f'{version} uploaded!', tab=True)

    echo_title(f'Downloaded: {len(downloaded)} version')
    for version in downloaded:
        echo_text(f'{version} downloaded!', tab=True)

    echo_completed()


@cli.command()
@click.argument('version', type=click.STRING, required=False, default=None)
@click.pass_context
def create(ctx, version):
    '''
        Create a local version
    '''
    resource = ctx.obj['resource']
    tools = ctx.obj['tools']

    echo_progresses()

    if version is None:
        echo_text(f'Create version auto name')
        version = tools.exec(resource, 'create_version')
    else:
        echo_text(f'Create version `{version}`')
        version = tools.exec(resource, 'create_version', version)

    echo_title(f'Created:')
    echo_text(f'{version} local', tab=True)
    echo_completed()


@cli.command()
@click.argument('version', type=click.STRING, required=True)
@click.pass_context
def extract(ctx, version):
    '''
        Extract local version to resource
    '''
    resource = ctx.obj['resource']
    tools = ctx.obj['tools']

    echo_progresses()
    echo_text(f'Extracting version `{version}` ...')

    tools.exec(resource, 'extract_version', version)

    echo_completed()


@cli.command()
@click.option('--local/--remote', default=None, help="Remove `local` or `remote`")
@click.option('--all', 'is_all', is_flag=True, help='Remove all')
@click.option('--yes', 'pass_confirm', is_flag=True, help='Auto pass rm --all confirm')
@click.argument('version', type=click.STRING, cls=RequiredConditionArgument, not_required_if="is_all", required_if=lambda ctx, opts, args: opts.get('is_all') is None)
@click.pass_context
def rm(ctx, local, is_all, pass_confirm, version):
    '''
        Remove version 
    '''
    resource = ctx.obj['resource']
    tools = ctx.obj['tools']

    echo_progresses()

    if is_all:

        echo_text('List version:')

        local_versions = tools.exec(
            resource, 'list_local_version') if local is None or local is True else []
        remote_versions = tools.exec(
            resource, 'list_drive_version') if local is None or local is False else []

        versions = [(version, 'local') for version in local_versions] + \
            [(version, 'remote') for version in remote_versions]

        versions.sort(key=lambda item: item[0])

        for version in versions:
            click.secho(f'{version[0]} {version[1]}', bold=True,
                        fg='blue' if version[1] == 'local' else 'green')

        if local is None:
            if not pass_confirm:
                click.confirm(
                    'Do you want to remove all local and remote version', abort=True)

            echo_title('Remove progress:')

            for version in local_versions:
                echo_text(f'Remove {version} local')
                tools.exec(resource, 'remove_local_version', version)

            for version in remote_versions:
                echo_text(f'Remove {version} remote')
                tools.exec(resource, 'remove_drive_version', version)

        elif local:

            if not pass_confirm:
                click.confirm(
                    'Do you want to remove all local version', abort=True)

            echo_title('Remove progress:')

            for version in local_versions:
                echo_text(f'Remove {version} local')
                tools.exec(resource, 'remove_local_version', version)

        else:

            if not pass_confirm:
                click.confirm(
                    'Do you want to remove all remote version', abort=True)

            echo_title('Remove progress:')

            for version in remote_versions:
                echo_text(f'Remove {version} remote')
                tools.exec(resource, 'remove_drive_version', version)

    else:
        if local is None:
            echo_text(f'Remove version `{version}` on local and remote')
            tools.exec(resource, 'remove_local_version', version)
            tools.exec(resource, 'remove_drive_version', version)

        elif local:
            echo_text(f'Remove version `{version}` on local')
            tools.exec(resource, 'remove_local_version', version)
        else:
            echo_text(f'Remove version `{version}` on remote')
            tools.exec(resource, 'remove_drive_version', version)

    echo_completed()


if __name__ == "__main__":
    cli()

# if __name__ == '__main__':
#     config_file = sys.argv[1]
#     args = sys.argv[2:]

#     config: dict = None

#     with open(config_file) as f:
#         config = json.load(f)

#     tools = BackupTools(config)

#     result = tools.exec(*args)

#     pprint.pprint(result)
