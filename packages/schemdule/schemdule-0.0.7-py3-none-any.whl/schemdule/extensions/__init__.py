from abc import ABC, abstractmethod
import logging
from types import ModuleType
from typing import Any, Dict, List, Set
import importlib
import pkgutil

EXTENSION_MODULE_PREFIX = "schemdule.extensions."

_logger = logging.getLogger("extensions")


def schemaEnvironment(env: Dict[str, Any]) -> None:
    pass


def find_extensions() -> List[str]:
    return [name.replace(EXTENSION_MODULE_PREFIX, "", 1) for finder, name, ispkg in pkgutil.iter_modules(__path__, EXTENSION_MODULE_PREFIX)]


def import_extension(full_name: str) -> ModuleType:
    _logger.debug(f"Import extension {full_name}.")
    return importlib.import_module(f"{full_name}.__reg__")


def load_extension(name: str) -> ModuleType:
    _logger.info(f"Load extension {name}.")
    return import_extension(f"schemdule.extensions.{name}")


def load_extensions(names: List[str]) -> List[ModuleType]:
    return [load_extension(name) for name in names]


def use_extension(extension: ModuleType, env: Dict[str, Any]) -> None:
    _logger.info(
        f"Use extension {extension.__name__.replace('__reg__', '', 1)}.")
    configFuncName = "schemaEnvironment"
    if hasattr(extension, configFuncName):
        func = getattr(extension, configFuncName)
        func(env)


def use_extensions(extensions: List[ModuleType], env: Dict[str, Any]) -> None:
    for extension in extensions:
        use_extension(extension, env)


def get_extension_metadata(extension: ModuleType) -> None:
    version = getattr(extension, "__version__", None)
    return {"version": version}
