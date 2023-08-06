"""Declares an interface to load editable text configuration."""
import os

import jinja2
import yaml

from unimatrix.const import ETCDIR
from .datastructures import DTO


environment = jinja2.Environment( # nosec
    autoescape=False,
    variable_start_string="${",
    variable_end_string="}"
)


def render(text, **params):
    """Renders the editable text configuration `text`."""
    t = environment.from_string(text)
    return t.render(env=os.environ, **params)


def load(path, *args, **kwargs) -> dict:
    """Loads the configuration from the specified path."""
    if not os.path.isabs(path):
        path = os.path.join(ETCDIR, path)
    if not os.path.exists(path):
        return None

    with open(path, 'r') as f:
        etc = render(f.read(), **kwargs)
    return DTO.fromdict(yaml.safe_load(etc))
