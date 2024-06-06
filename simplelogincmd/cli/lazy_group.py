"""
Lazy-loading Click group and utils
"""

import click


def cmd_path(file: str, *args: str) -> str:
    """
    Util to construct a path to a LazyGroup's subcommands

    The final path is the parent directory of `file` joined with all
    the subdirectories in `args`. An example of common usage follows:

    .. code-block:: python

       @click.group(
           "group_name",
           cls=LazyGroup,
           cmd_path=cmd_path(__file__, "subdir"),
       )
       def cli():
           pass

    If `__file__` above points to "/foo/bar.py", then the path at which
    the group's subcommands live is defined as "/foo/subdir/".

    :param file: The path to a file, usually the one in which the
        group is located
    :type file: str
    :param args: One or more subdirectories relative to that containing
        `file` in which the group's subcommands are located
    :type arg: str

    :return: The directory in which a LazyGroup's subcommands are
        located
    :rtype: str
    """
    import os

    return os.path.join(os.path.dirname(file), *args)


class LazyGroup(click.Group):
    """
    A Click group that lazily loads its subcommands

    Overridden methods:

    - list_commands
    - get_command

    Both are overridden by lazy implementations
    """

    def __init__(self, *args, cmd_path: str, **kwargs) -> None:
        """
        Constructor

        :param cmd_path: The directory in which the group's subcommands
            are located
        :type cmd_path: str
        """
        super().__init__(*args, **kwargs)
        self._cmd_path = cmd_path

    def list_commands(self, context) -> list[str]:
        import os

        commands = []
        for file in os.listdir(self._cmd_path):
            if file.endswith(".py") and not file.startswith("_"):
                module = file[:-3]
                commands.append(module)
        commands.sort()
        return commands

    def get_command(self, context, name):
        import importlib.util
        import os

        path = os.path.join(self._cmd_path, f"{name}.py")
        spec = importlib.util.spec_from_file_location(name, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return getattr(module, name)
