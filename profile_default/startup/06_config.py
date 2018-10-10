import os
from configparser import ConfigParser
import IPython

cfg_parser = ConfigParser()
cfg_parser.optionxform = str    # to have case sensitive var names

# noinspection PyUnresolvedReferences
profile_default_path = IPython.paths.locate_profile()

cfg_parser.read(os.path.join(profile_default_path, 'startup', '.sys_env.cfg'), encoding='utf-8')
