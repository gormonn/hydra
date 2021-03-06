# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from typing import List, Optional

from omegaconf import DictConfig, open_dict

from hydra._internal.hydra import Hydra
from hydra._internal.utils import detect_calling_file_or_module_from_stack_frame
from hydra.core.global_hydra import GlobalHydra


def initialize(
    config_path: Optional[str] = None,
    strict: Optional[bool] = None,
    caller_stack_depth: int = 1,
) -> None:
    """
    Initialize automatically detect the calling file or module.
    config_path is relative to the detected calling for or module.

    :param config_path: A directory relative to the declaring python file or module
    :param strict: (Deprecated), will be removed in the next major version
    :param caller_stack_depth: stack depth of module the config_path is relative to
    """
    calling_file, calling_module = detect_calling_file_or_module_from_stack_frame(
        caller_stack_depth + 1
    )
    Hydra.create_main_hydra_file_or_module(
        calling_file, calling_module, config_path, strict
    )


def initialize_with_file(
    calling_file: Optional[str], config_path: Optional[str] = None
) -> None:
    """
    Initialize Hydra and add the config_path to the search path.
    The config path is relative to the calling_file.
    :param calling_file : The file to make the config_path relative to
    :param config_path : The config path
    """
    Hydra.create_main_hydra_file_or_module(calling_file, None, config_path, None)


def initialize_with_module(
    calling_module: Optional[str], config_path: Optional[str] = None
) -> None:
    """
    Initialize Hydra and add the config_path to the search path.
    The config path is relative to the calling_module.
    :param calling_module : The module to make the config_path relative to
    :param config_path : The config path
    """

    Hydra.create_main_hydra_file_or_module(None, calling_module, config_path, None)


def compose(
    config_name: Optional[str] = None,
    overrides: List[str] = [],
    strict: Optional[bool] = None,
) -> DictConfig:
    """
    :param config_name: the name of the config (usually the file name without the .yaml extension)
    :param overrides: list of overrides for config file
    :param strict: optionally override the default strict mode
    :return: the composed config
    """
    assert (
        GlobalHydra().is_initialized()
    ), "GlobalHydra is not initialized, use @hydra.main() or call hydra.experimental.initialize() first"

    gh = GlobalHydra.instance()
    assert gh.hydra is not None
    cfg = gh.hydra.compose_config(
        config_name=config_name, overrides=overrides, strict=strict
    )
    assert isinstance(cfg, DictConfig)

    if "hydra" in cfg:
        with open_dict(cfg):
            del cfg["hydra"]
    return cfg
