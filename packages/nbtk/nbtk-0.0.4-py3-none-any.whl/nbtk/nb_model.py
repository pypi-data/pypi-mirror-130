
import logging
import yaml

class Model(yaml.YAMLObject):
    yaml_tag = 'model'

    def __init__(self
                 , name
                 , author=None
                 , version=None
                 , type=None
                 , field=None
                 , dependencies=None
                 , train_req=None
                 , inference_req=None
                 , param_file=None
                 , metrics=None
                 , summary=None
                 , keyword=None
                 , desc=None
                 , reference=None
                 , cite=None
                 ):

        self.name = name
        self.author = author
        self.version = version
        self.type = type
        self.field = field
        self.dependencies = dependencies
        self.train_req = train_req
        self.inference_req = inference_req
        self.param_file = param_file
        self.metrics = metrics
        self.summary = summary
        self.keyword = keyword
        self.desc = desc
        self.reference = reference
        self.cite = cite


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