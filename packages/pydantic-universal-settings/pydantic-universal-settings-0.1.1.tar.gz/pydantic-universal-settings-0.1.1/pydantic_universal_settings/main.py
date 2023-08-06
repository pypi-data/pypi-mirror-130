import abc
import json
import os
import tempfile
from pathlib import Path
from typing import Any, Dict, Generic, Iterable, List, Optional, Type, TypeVar, Union

from psutil import pid_exists
from pydantic import BaseModel, BaseSettings as PydanticBaseSettings, root_validator
from pydantic_universal_settings import logger

_global_settings_models_dict: Dict[str, Type[BaseModel]] = {}
_global_settings_models_names: List[str] = []


def add_settings(name: Optional[Union[str, Type[BaseModel]]] = None) -> Any:
    def decorator(cls: Type[BaseModel]) -> Type[BaseModel]:
        if isinstance(name, str) and name:
            model_name = name
        else:
            model_name = cls.__name__
        if model_name in _global_settings_models_dict:
            raise KeyError(f"Error: settings {model_name} already added!")
        # else:
        #     print(model_name)
        _global_settings_models_dict[model_name] = cls
        _global_settings_models_names.append(model_name)
        return cls

    if name is None or isinstance(name, str):
        return decorator
    else:
        return decorator(name)


def parse_settings_models(
    settings_models: Union[None, str, Iterable[str]]
) -> List[Type[BaseModel]]:
    _settings_models = []
    if settings_models is None:
        _settings_models = _global_settings_models_names
    elif isinstance(settings_models, str):
        _settings_models = [settings_models]
    elif isinstance(settings_models, Iterable):
        _settings_models = list(settings_models)
    result = []
    for model_name in _settings_models:
        if model_name not in _global_settings_models_dict:
            raise KeyError(f"Error: settings {model_name} not added!")
        result.append(_global_settings_models_dict[model_name])
    return result


class BaseSettings(BaseModel, abc.ABC):
    pass


T = TypeVar("T", bound=BaseSettings)


class EnvFileMixin(BaseSettings):
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


class CLIMixin(BaseModel):
    @staticmethod
    def _save(cli_settings: Dict[str, Any]) -> None:
        return

    @staticmethod
    def _load() -> Dict[str, Any]:
        return {}

    @root_validator(allow_reuse=True)
    def _inject_cli(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        from pydantic_universal_settings.cli import cli_settings

        if "__not_empty" in cli_settings:
            del cli_settings["__not_empty"]
            _cli_settings = cli_settings
            cls._save(cli_settings)
        else:
            _cli_settings = cls._load()
        for key, value in _cli_settings.items():
            if key in values and not key.startswith("__") and value is not None:
                values[key] = value
        return values


class CLIWatchMixin(CLIMixin):
    _temp_settings_file: Optional[str] = None

    @staticmethod
    def _save(cli_settings: Dict[str, Any]) -> None:
        if len(cli_settings) == 0:
            return
        tempdir = Path(tempfile.gettempdir()) / "fastapi_rest_framework"
        tempdir.mkdir(exist_ok=True)
        # delete previous settings files if the process doesn't exist
        for file in tempdir.glob("*.settings.json"):
            try:
                pid = int(file.name.split(".")[0])
                if not pid_exists(pid):
                    file.unlink(missing_ok=True)
            except:  # noqa
                pass
        file_path = tempdir / f"{os.getpid()}.settings.json"
        with open(file_path, "w") as fp:
            json.dump(cli_settings, fp)
        logger.info("Save command line options into {}.", file_path)

    @staticmethod
    def _load() -> Dict[str, Any]:
        tempdir = Path(tempfile.gettempdir()) / "pydantic_universal_settings"
        file_path = tempdir / f"{os.getppid()}.cli.json"
        try:
            with open(file_path) as fp:
                data = json.load(fp)
            logger.info("Load command line options from {}.", file_path)
            return data
        except:  # noqa
            return {}


def generate_all_settings(
    settings_models: Union[None, str, Iterable[str]] = None,
    name: Optional[str] = None,
    mixins: Optional[List[type]] = None,
) -> Type[T]:
    if not name:
        name = "UniversalSettings"
    if mixins is None:
        mixins = []
    base_classes = parse_settings_models(settings_models)
    new_class = type(
        name,
        (
            *mixins,
            *base_classes,
            PydanticBaseSettings,
        ),
        {},
    )
    return new_class  # type: ignore


class SettingsProxy(Generic[T]):
    def __init__(self) -> None:
        self._settings: Optional[T] = None

    def __getattr__(self, attr: str) -> Any:
        if attr in self.__dict__:
            return self.__dict__[attr]
        if self._settings is None:
            raise ValueError("settings not initialized")
        return getattr(self._settings, attr)

    def __str__(self) -> str:
        return str(self._settings)

    def __repr__(self):
        return repr(self._settings)


def init_settings(
    settings_cls: Type[T], overwrite: bool = True
) -> Union[T, SettingsProxy[T]]:
    _settings = getattr(settings, "_settings", None)
    if _settings is None or overwrite:
        _settings = settings_cls()
        setattr(settings, "_settings", _settings)
    return _settings


settings: Union[BaseSettings, SettingsProxy[Any]] = SettingsProxy()


def get_settings_proxy():
    return settings
