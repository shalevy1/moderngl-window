"""
Bag of settings values
"""
import importlib
import os
from moderngl_window.conf import default
from moderngl_window.exceptions import ImproperlyConfigured

SETTINGS_ENV_VAR = "MODERNGL_WINDOW_SETTINGS_MODULE"

# pylint: disable=C0103


class Settings:
    """
    Bag of settings values.
    New attributes can be freely added (values or functions)
    """
    def __init__(self):
        """Initialize settins with default values"""
        # Set default entires. Mainly for code completion
        self.WINDOW = None
        # Finders
        self.PROGRAM_FINDERS = None
        self.TEXTURE_FINDERS = None
        self.SCENE_FINDERS = None
        self.DATA_FINDERS = None
        # Finder dirs
        self.PROGRAM_DIRS = None
        self.TEXTURE_DIRS = None
        self.SCENE_DIRS = None
        self.DATA_DIRS = None
        # Loaders
        self.PROGRAM_LOADERS = None
        self.TEXTURE_LOADERS = None
        self.SCENE_LOADERS = None
        self.DATA_LOADERS = None

        self.apply_default_settings()

    def setup(self, setting_module=None, settings_module_name=None, **kwargs):
        """
        Apply settings values from various sources

        Keyword Args:
            settings_module (module): Reference to a settings module
            settings_module_name (str): Full pythonpath to a settings module
        """
        settings_module_name = settings_module_name or os.environ.get(SETTINGS_ENV_VAR)
        if not setting_module:
            module = importlib.import_module(settings_module_name)
            if not module:
                raise ImproperlyConfigured(
                    "Settings module '{}' not found. ".format(settings_module_name)
                )

        if setting_module:
            self.apply_module(setting_module)

        self.apply_dict(kwargs)

    def update(self, **kwargs):
        """Override settings values"""
        for name, value in kwargs.items():
            setattr(self, name, value)

    def apply_default_settings(self):
        """Apply keys and values from the default settings module"""
        for setting in dir(default):
            if setting.isupper():
                setattr(self, setting, getattr(default, setting))

    def apply_dict(self, data):
        for name, value in data.items():
            setattr(self, name, value)

    def apply_module(self, module):
        for setting in dir(module):
            if setting.isupper():
                value = getattr(module, setting)
                # TODO: Add more validation here
                setattr(self, setting, value)

    def __repr__(self):
        return '<{cls} "{data}>"'.format(
            cls=self.__class__.__name__,
            data=None,
        )


settings = Settings()