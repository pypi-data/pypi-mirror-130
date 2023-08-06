import os
import toml
from pathlib import Path

from .exceptions import RelyComplyClientException

keys = ["token", "url", "impersonate"]


def merge_credentials(layers):
    credentials = {}
    for layer_credentials in layers:
        credentials.update(layer_credentials)
    return credentials


class Default:
    def credentials(self):
        return {"url": "https://app.relycomply.com"}


class Environment:
    def credentials(self):
        return {
            key: os.environ[f"RELYCOMPLY_{key.upper()}"]
            for key in keys
            if f"RELYCOMPLY_{key.upper()}" in os.environ
        }


class ConfigFolder:
    def __init__(self, folder: Path):
        self.folder = folder

    def credentials(self):
        config_path = self.folder / ".rely.toml"
        if not config_path.exists():
            return {}
        else:
            with open(config_path) as f:
                try:
                    config_values = toml.load(f)
                    # TODO Check for string
                    return {
                        key: config_values[key] for key in keys if key in config_values
                    }
                except:
                    pass


class Config:
    def credentials(self):

        root = Path(".").resolve()
        folder_credentials = []
        while root:
            folder_credentials.insert(0, ConfigFolder(root).credentials())
            if root == root.parent:
                break
            root = root.parent
        return merge_credentials(folder_credentials)


class Arguments:
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def credentials(self):
        return {key: self.kwargs[key] for key in keys if self.kwargs.get(key)}


class StandardCredentials:
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        loaders = [
            Default(),
            Config(),
            # Environment(),
            Arguments(**self.kwargs),
        ]
        layers = [loader.credentials() for loader in loaders]
        self.results = merge_credentials(layers)

    def credentials(self):
        return self.results

    def get(self, key):
        return self.credentials().get(key)

    def require(self, key):
        value = self.get(key)
        if not value:
            raise RelyComplyClientException(
                f"Credential '{key}' is required but not present"
            )
        return value
