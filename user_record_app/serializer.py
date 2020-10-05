from abc import abstractmethod
import json

import yaml

class Serializer(object):
    """
    Base Serializer class that is used to serialize data into a desired format.
    """
    def __init__(self, dict={}):

        self.dict = dict

    @abstractmethod
    def serialize(self):
        """
        Serializes a dict into a desired format. Requires implementation.
        """
        pass

class JsonSerializer(Serializer):
    """
    Serializer class that is used to serialize data into json.
    """
    def serialize(self):

        return json.dumps(self.dict)

class YamlSerializer(Serializer):
    """
    Serializer class that is used to serialize data into yaml.
    """
    def serialize(self):

        return yaml.dump(self.dict)
