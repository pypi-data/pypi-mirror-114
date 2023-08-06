"""Provides functions to configure secrets."""
from unimatrix.lib import etc

from .registry import registry


def load():
    """Load secret configurations from editable text."""
    for alias, params in dict.items(etc.load('secrets.conf') or {}):
        registry.add({**params, 'alias': alias})
