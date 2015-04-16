from sourcerer.base import Document
from sourcerer.simple_statements import ReturnObj, Docstring
from sourcerer.callables import FunctionObj, DecoratorObj
from sourcerer.syntaxes import base_map, yaml_map
from sys import stdout, argv
import yaml
"""
r = RouteFunctionObj(name="test_route")
ret = ReturnObj
ret = ReturnObj()
dec = RouteDecoratorObj(name="route", arg_names=["/products"])

doc = Document()
doc.add_children(route([dec], r, ret))
doc.export()
"""
class DefaultProcessor(object):

    def __init__(self, parser=None):
        """ Create a default empty Document

        Args:
            parser (function): The function to parse the file ex. yaml.load, json.loads
        """
        self.doc = Document()
        self.map = base_map
        self.parser = parser if parser is not None else lambda x: {}

    def load(self, file_name=None, doc=None):
        """ Parse a specification file into a deserialized format
        
        Args:
            file_name (str): The name of the spec file to load as a string
            doc (Document): A pre-built Document
        """
        if doc is not None:
            if isinstance(doc, Document):
                self.doc = doc
        else:
            if file_name is not None and parser is not None:
                loader = loader if loader is not None else lambda x: {}
                self.file_name = file_name
                with open(self.file_name, 'r') as my_file:
                    self.parsed_data = self.parser(my_file)
                self.assemble(self.parsed_data)

    def assemble(self, parsed_data):
        """ Process all the nodes in a parsed input document
        
            Feel free to overload this, but you may want to write a new
            syntax map instead.
        """
        if not isinstance(parsed_data, dict):
            raise TypeError()
        for key in parsed_data.keys():
            if key in self.map.keys():
                self.map[key]
        """
        if not isinstance(value, dict):
            if key in self.map.keys():
                obj = self.map.get(key)
                params = {param_key:param_val for param_key, param_val in self.assemble(value)}
                yield {key:obj(**params)}
        else:
            for key, value in data.items():
                yield self.assemble(key, value)
        """

    def output(self, output_file_name=''):
        """ Write out the syntax tree """
        syntax_string = ''.join(self.doc)
        if not output_file_name:
            stdout.write(syntax_string)
        else:
            with open(output_file_name, 'w') as output:
                output.write(syntax_string)

class YAMLProcessor(DefaultProcessor):
    """ A processor that builds a Document from a YAML file """

    def __init__(self):
        super(YAMLProcessor, self).__init__()
        self.parser = yaml.load

    def assemble(self, ast):
        """ Build a Document from yaml """
            




if __name__ == "__main__":
    gen = DefaultProcessor()
    gen.build_from(argv[1])
    gen.output()
