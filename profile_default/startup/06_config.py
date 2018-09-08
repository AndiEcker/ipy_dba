import os
from configparser import ConfigParser
import IPython

cfg_parser = ConfigParser()
cfg_parser.optionxform = str    # to have case sensitive var names
# noinspection PyUnresolvedReferences
cfg_parser.read(os.path.join(IPython.paths.locate_profile(), 'startup', '.sys_env.cfg'), encoding='utf-8')
