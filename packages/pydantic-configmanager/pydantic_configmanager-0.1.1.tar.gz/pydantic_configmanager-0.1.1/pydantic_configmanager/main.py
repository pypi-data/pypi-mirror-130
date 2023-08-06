from os import environ
from typing import Any, TypeVar, Union, AbstractSet, List, Dict, Type, Sequence, Optional, Any

from pydantic import BaseSettings, BaseConfig, Extra, BaseModel
from pydantic.errors import DecimalMaxDigitsError
from pydantic.fields import FieldInfo, ModelField
from pydantic.typing import display_as_type
from pydantic.utils import sequence_like
import warnings


T = TypeVar('T', bound='EnvironmentBaseModel')


class EnvFieldInfo(BaseModel):
    names: List[str]
    type: str
    description: Optional[str]
    default: Any


def get_model_env_info(model: Type[BaseModel]):
    fields: Dict[str, ModelField] = model.__fields__
    env_vars: List[EnvFieldInfo] = []
    for fieldname, field in fields.items():
        _ = fieldname
        env_field_info = EnvFieldInfo(
            names=field.field_info.extra.get('env_names', {}),
            type=field.type_.__name__,
            description=field.field_info.description or fieldname,
            default=field.default
        )
        env_vars.append(env_field_info)
    return env_vars

def env_translation(model: Type[BaseSettings]) -> Dict[str, str]:
    fields: Dict[str, ModelField] = model.__fields__
    translation_map: Dict[str, str] = dict()
    for fieldname, field in fields.items():
        names = field.field_info.extra.get('env_names',dict())
        for name in names:
            translation_map[name] = fieldname
    return translation_map



class SettingsConfig(BaseConfig):

    allow_population_by_field_name = True
    env_prefix = ''
    name_prefix = ''
    env_postfix = ''
    env_file = None
    env_file_encoding = None
    secrets_dir = None
    validate_all = True
    extra = Extra.allow
    arbitrary_types_allowed = True
    case_sensitive = False

    @classmethod
    def env_alias_generator(cls, fieldname: str) -> str:
        """Create environment names with a name prefix, env prefix and a postfix."""
        env = str(cls.env_prefix)
        name = str(cls.name_prefix)
        if env and not env.endswith("_"):
            env = f"{env}_"
        if name and not name.endswith("_"):
            name = f"{name}_"

        return f'{cls.name_prefix}{env}{fieldname}{cls.env_postfix}'.upper()

    @classmethod
    def prepare_field(cls, field: ModelField) -> None:
        env_names: Union[List[str], AbstractSet[str]]
        field_info_from_config = cls.get_field_info(field.name)

        env = field_info_from_config.get('env') or field.field_info.extra.get('env')
        if env is None:
            if field.has_alias:
                warnings.warn(
                    'aliases are no longer used by BaseSettings to define which environment variables to read. '
                    'Instead use the "env" field setting. '
                    'See https://pydantic-docs.helpmanual.io/usage/settings/#environment-variable-names',
                    FutureWarning,
                )
            env_names = {cls.env_alias_generator(field.name)}
        elif isinstance(env, str):
            env_names = {env}
        elif isinstance(env, (set, frozenset)):
            env_names = env
        elif sequence_like(env):
            env_names = list(env)
        else:
            raise TypeError(f'invalid field env: {env!r} ({display_as_type(env)}); should be string, list or set')

        if not cls.case_sensitive:
            env_names = env_names.__class__(n.upper() for n in env_names)
        field.field_info.extra['env_names'] = env_names


class EnvironmentBaseModel(BaseSettings):
    """
    Pydantic BaseSettings class with extended environment variable generation and template output.

    This is useful in production for secrets you do not wish to save in code, it plays nicely with docker(-compose),
    Heroku, Kubernetes, Openshift and any 12 factor app design.
    """

    class Config(SettingsConfig):
        """Configuratio for the Config class via a... Config class."""


    @classmethod
    def env_config(cls, by_alias: bool = True, include_export: bool = False) -> str:
        """Return settings template as they would go into environment."""
        export = ''
        env_fields = get_model_env_info(cls)
        if include_export:
            export = "export "
        schema = cls.schema(by_alias)
        output: str = f"# {schema.get('description','')}\n"
        output += '# -----\n'
        output += '# These are the supported environment configuration variables.\n'
        output += '# Set these up in your environment.\n'
        output += '\n'
        for field in env_fields:
            type_value = field.type
            if type_value:  # if a type is set, format the output:
                type_value = f"; type: {type_value}"
            default_value = field.default
            default_repr = ''  #
            if default_value:
                default_repr = f"{default_value!a}"
            description = f"{field.description}"
            comment = f"  # {description}{type_value}"
            name = field.names[0]
            output_line = f"{export}{name}={default_repr}{comment}\n"
            output += output_line
        return output

    @classmethod
    def from_env(cls, **data: Any) -> T:
        """Initialize object from environmnent variables."""
        data = data or dict()
        env_mapping = env_translation(cls)
        for env_name, field_name in env_mapping.items():
            if env_name in environ and not data.get(field_name, None):
                data[field_name] = environ.get(env_name)
        return cls(**data)  # type: ignore
