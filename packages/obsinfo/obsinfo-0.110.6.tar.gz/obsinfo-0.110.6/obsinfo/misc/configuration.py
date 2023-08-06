import os
import sys
import re
from pathlib import Path
import warnings
warnings.simplefilter("once")
warnings.filterwarnings("ignore", category=DeprecationWarning)
import yaml

class Singleton:

    def __init__(self, cls):
        self._cls = cls

    def Instance(self):
        try:
            return self._instance
        except AttributeError:
            self._instance = self._cls()
            return self._instance

    def __call__(self):
        raise TypeError('Singletons must be accessed through `Instance()`.')

    def __instancecheck__(self, inst):
        return isinstance(inst, self._cls)
 
@Singleton
class ObsinfoConfiguration:
        
    def __init__(self):
        """
        Read .obsinforc file and setup the configuration
        """
        home = Path.home()
        config_file = Path(home).joinpath(".obsinforc")
        # This is called directly to avoid the paraphernalia of yamlref.
        try:
            with open(config_file, "r") as fp:
               config_dict = yaml.safe_load(fp)
        except FileNotFoundError:
            warnings.warn("Configuration file .obsinforc not found. Run obsinfo-setup")
            raise
        except OSError:
            warnings.warn("Operating system error reading configuration file .obsinforc")
            raise 
        
        self.obsinfo_datapath = config_dict.get("datapath", "")
        self.gitlab_repository = config_dict.get("gitlab_repository", "")
        self.gitlab_project = config_dict.get("gitlab_project", "")
        self.gitlab_path = config_dict.get("gitlab_path", "")
        self.obsinfo_version = str(config_dict.get("obsinfo_version", ""))
        
