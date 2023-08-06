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

    # def __repr__(self):
    #     return '%s(name=%s, age=%d)' % (self.__class__.__name__, self.name, self.age)

# model = Model(name='James', version=20, train_req={"executable":"train.py","outputs":["a","b","c"]})
#
# with open('../../tests/data1.yml', 'w') as outfile:
#     yaml.dump(model, outfile, default_flow_style=False)

# lily = yaml.load('!person {name: Lily, age: 19}')
#
# print (lily)  # yaml转为Python对象实例