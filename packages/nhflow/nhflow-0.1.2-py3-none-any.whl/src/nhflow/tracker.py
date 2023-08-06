
import logging
from model import Model
import yaml

_logger = logging.getLogger(__name__)


def _def_param():
	print(1)


def _log_metric():
	print(2)

def _set_name(name):
	my_model = Model(name = name)
	with open('mymodel.yml', 'w') as outfile:
		yaml.dump(my_model, outfile, default_flow_style=False)
	logging.info("yaml file dumped")