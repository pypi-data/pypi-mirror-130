from dataclasses import dataclass


@dataclass
class CliContext:
    """Class for keeping track of global options."""

    debug: bool = False
