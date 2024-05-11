"""This module helps to lazy loading a python module"""

import importlib
from types import ModuleType
from typing import Any


class LazyImporter:
    """Allow to lazy load a python module"""

    def __init__(self, module_name: str) -> None:
        self.module_name = module_name

    def get_module(self) -> ModuleType:
        """Load the whole module using the full name"""
        return importlib.import_module(self.module_name)

    def get_config_class(self, config_name: str) -> Any:
        """Load a config class inside a module, given the args"""
        module = self.get_module()
        return getattr(module, config_name)
