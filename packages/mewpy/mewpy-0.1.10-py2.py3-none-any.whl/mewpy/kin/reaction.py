from collections import OrderedDict


class KineticModel(object):

    def __init__(self,
                 name='unnamed',
                 reactions=None):

        self.name = name
        self.reactions = OrderedDict(reactions) if hasattr(myObj, '__iter__') else OrderedDict()
        
