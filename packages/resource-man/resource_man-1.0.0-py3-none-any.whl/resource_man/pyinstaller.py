import os
import types
import contextlib
from .importlib_interface import \
    USING_IMPORTLIB, USING_IMPORTLIB_RESOURCES, USING_RESOURCE_MAN, Traversable, \
    files, as_file, read_binary, read_text, contents, is_resource
from .interface import ResourceNotAvailable, Resource, register, has_resource, get_resources, get_resource, \
    get_binary, get_text
try:
    from importlib.machinery import SOURCE_SUFFIXES
except (ImportError, Exception):
    SOURCE_SUFFIXES = ['.py', '.pyw', '.py2', '.py3']


__all__ = [
    'collect_datas', 'EXCLUDE_EXT', 'SOURCE_SUFFIXES',
    'USING_IMPORTLIB', 'USING_IMPORTLIB_RESOURCES', 'USING_RESOURCE_MAN', 'Traversable',
    'files', 'as_file', 'read_binary', 'read_text', 'contents', 'is_resource',
    'ResourceNotAvailable', 'Resource', 'register', 'has_resource', 'get_resources', 'get_resource',
    'get_binary', 'get_text'
    ]


EXCLUDE_EXT = SOURCE_SUFFIXES + ['.pyc', '.pyd']


def collect_datas(package, exclude_ext=None, **kwargs):
    """Collect data files for pyinstaller.

    Args:
        package (types.ModuleType/str/Traversable): Top level package module or module name.
        exclude_ext (list)[None]: List of extensions to not include in the pyinstaller data.

    Returns:
        datas (list): List of (abs file path, rel install path). This will also include subdirectories.
    """
    if exclude_ext is None:
        exclude_ext = EXCLUDE_EXT

    datas = []
    pkg_name = package
    if isinstance(package, types.ModuleType):
        pkg_name = package.__package__

    with contextlib.suppress(ImportError, Exception):
        toplvl = files(package)
        with as_file(toplvl) as n:
            toplvl_filename = str(n)  # n should be a Path object, but I noticed it was a str anyway
        subdirs = [toplvl]
        while True:
            try:
                directory = subdirs.pop(0)
            except IndexError:
                break

            for path in directory.iterdir():
                if path.name == '__pycache__':
                    continue

                if path.is_dir():
                    # Add subpackage
                    subdirs.append(path)
                elif path.suffix not in exclude_ext:
                    # Assume this is a resource.
                    with as_file(path) as filename:
                        relpath = os.path.join(pkg_name, os.path.relpath(filename, toplvl_filename))
                        data = (str(filename), os.path.dirname(relpath))
                        if data not in datas:
                            datas.append(data)

    return datas
