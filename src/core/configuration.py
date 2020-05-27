"""configuration module
"""

import yaml 


CFG_FILE_ = './src/config.yml'


def load_config_file(path=CFG_FILE_):
	with open(path, 'r') as f:
		cfg = yaml.load(f.read(), Loader=yaml.Loader)

	return cfg

