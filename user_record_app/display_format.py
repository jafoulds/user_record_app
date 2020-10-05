from abc import abstractmethod

from flask import jsonify, render_template

class DisplayFormat(object):
    """
    Base class that is used to display data in a desired display format
    such as text or html.
    """
    def __init__(self, dict={}):

        self.dict = dict

    @abstractmethod
    def display(self):
        """
        Function to be implemented that will display the data in the desired
        output format.
        """
        pass

class TextDisplayFormat(DisplayFormat):
    """
    Class used to display data in text form (json).
    """
    def display(self):

        return jsonify(self.dict)

class HtmlDisplayFormat(DisplayFormat):
    """
    Class used to display data in html.
    """
    def display(self):

        return render_template("dict_display.html", dict=self.dict)
