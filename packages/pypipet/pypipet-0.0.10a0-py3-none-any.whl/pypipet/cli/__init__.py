import click, logging
from .cli import cli
from pypipetcore.logging import setup_logging

from . import ( 
    init,
    catalog,
    product,
    template,
    order,
    inventory,
    fulfillment,
    static
)
