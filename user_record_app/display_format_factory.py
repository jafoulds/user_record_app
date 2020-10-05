from .display_format import HtmlDisplayFormat, TextDisplayFormat
from .singleton import Singleton

class DisplayFormatFactory(metaclass=Singleton):
    """
    This is an implementation of a factory design pattern that will generate
    the respective object for the specified display format.
    """
    def __init__(self):

        self.display_format_dict = {}
        # add text and html display formats by default
        self.register_format("TEXT", TextDisplayFormat)
        self.register_format("HTML", HtmlDisplayFormat)

    def register_format(self, format, creator):
        """
        Adds a dictionary entry to the display_format_dict with a key, value
        of format, object respectively.
        """
        self.display_format_dict[format] = creator

    def get_display(self, format):
        """
        Retrieves the object to create based on the given display format in
        string form.
        """
        creator = self.display_format_dict.get(format.upper())
        if not creator:
            raise ValueError(format)

        return creator()
