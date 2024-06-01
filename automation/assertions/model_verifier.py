""" Aux class to hold model name and expected attribute types"""

from typing import Dict


class ModelVerifier:
    """Aux class to hold model name and expected attribute types"""

    def __init__(self, name: str, data_args: Dict[str, any]) -> None:
        self.name = name
        self.data_args = data_args
