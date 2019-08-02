import importlib
import os

from configuration import __init_logging

env = os.environ.get("env", "dev")
supported_envs = ["dev", "test"]

__init_logging()

if env not in supported_envs:
    raise EnvironmentError("Unsupported environment: " + env)

module = importlib.import_module(f'configuration.{env}_configuration')
class_name = f'{env}Configuration'

class_attr = None
for attr in dir(module):
    if attr.lower() == class_name.lower():
        class_attr = attr
if not class_attr:
    raise ValueError(f'configuration class not found for env {env}')
configuration = getattr(module, class_attr)()

configuration.read_configuration()

backend_url = configuration.backend_url
