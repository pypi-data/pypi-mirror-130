from copy import deepcopy
import json
from typing import Any, Dict, io

import click
import yaml

DISK_SIZE_ERROR_MSG = "Invalid disk size, should be greater than 100Gb"


def validate_config(cfg: Dict[str, Any]) -> None:
    """
    Validates Grid config.

    Parameters
    ----------
    cfg: Dict[str, Any]
        Dictionary representing a Grid config
    """
    disk_size = cfg['compute']['train'].get('disk_size')
    if disk_size is not None and disk_size < 100:
        raise click.ClickException(DISK_SIZE_ERROR_MSG)


def read_config(value: io.TextIO):
    """
    Parameters
    ----------
    value:
        A TextIO object that has `.read()` defined for it
    """
    grid_config = value
    if grid_config:
        #  Loads the YML file as passed by the
        #  user.
        try:
            grid_config = yaml.safe_load(value.read())
            if not isinstance(grid_config, dict):
                raise Exception("Unexpected file structure")
        except Exception as e:
            raise click.BadParameter(f'Could not load your YAML config file: {e}')

        #  Adds required structure to the base
        #  YML file, if that structure isn't there.
        if 'compute' not in grid_config:
            grid_config['compute'] = {}
        if 'train' not in grid_config['compute']:
            grid_config['compute']['train'] = {}
    return grid_config


def read_config_callback(ctx, param, value):
    """
    Click callback that reads value from the config file and fix
    the structure if it doesn't exist.
    """
    return read_config(value)


def validate_disk_size_callback(ctx, param, value: int) -> int:
    """
    Validates the disk size upon user input.

    Parameters
    ----------
    ctx
        Click context
    param
        Click parameter
    value: int

    Returns
    --------
    value: int
        Unmodified value if valid
    """
    if value < 100:
        raise click.BadParameter(DISK_SIZE_ERROR_MSG)

    return value


def _duplicate_checker(js):
    result = {}
    for name, value in js:
        if name in result:
            raise ValueError('Failed to load JSON: duplicate key {0}.'.format(name))
        result[name] = value
    return result


def string2dict(text):
    if not isinstance(text, str):
        text = text.decode('utf-8')
    try:
        js = json.loads(text, object_pairs_hook=_duplicate_checker)
        return js
    except ValueError as e:
        raise ValueError('Failed to load JSON: {0}.'.format(str(e)))


def is_openapi(obj):
    return hasattr(obj, "swagger_types")


def create_openapi_object(json_obj: Dict, target: Any):
    """ Create the openAPI object from the given json dict and based on the target object
    We use the target object to make new object from the given json spec and hence target
    must be a valid object.
    """
    if not isinstance(json_obj, dict):
        raise TypeError("json_obj must be a dictionary")
    if not is_openapi(target):
        raise TypeError("target must be an openapi object")

    target_attribs = {}
    for key, value in json_obj.items():
        try:
            # user provided key is not a valid key on openapi object
            sub_target = getattr(target, key)
        except AttributeError:
            raise ValueError(f"Field {key} not found in the target object")

        if is_openapi(sub_target):  # it's an openapi object
            target_attribs[key] = create_openapi_object(value, sub_target)
        else:
            target_attribs[key] = value

        # TODO(sherin) - specifically process list and dict and do the validation. Also do the
        #  verification for enum types

    new_target = target.__class__(**target_attribs)
    return new_target
