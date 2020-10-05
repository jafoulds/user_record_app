from .serializer import JsonSerializer, YamlSerializer
from .singleton import Singleton

class SerializerFactory(metaclass=Singleton):
    """
    This is an implementation of a factory design pattern that will generate
    the respective object for the specified serializer format.
    """
    def __init__(self):

        self.serializer_format_dict = {}
        # add json and yaml as default serializer formats
        self.register_format("JSON", JsonSerializer)
        self.register_format("YAML", YamlSerializer)

    def register_format(self, format, creator):
        """
        Adds a dictionary entry to the serializer_format_dict with a key, value
        of format, object respectively.
        """

        self.serializer_format_dict[format] = creator

    def get_serializer(self, format):
        """
        Retrieves the object to create based on the given serializer format in
        string form.
        """
        creator = self.serializer_format_dict.get(format.upper())
        if not creator:
            raise ValueError(format)

        return creator()
