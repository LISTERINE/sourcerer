#!env/bin/python
from pdb import set_trace
from formatters import Formatter
from sys import stdout


class Statement(object):
    """ A line of code 
    
    A Statement is a line of code that may or may not have a child Scope
    """

    def __init__(self, code='', scope=None, whitespace='', line_ending='\n'):
        """
        self.code is the actual line of code that this object represents.
        self.scope (if any) is the child scope of this statement. eg.
         self.code ->   while 1:
                        {   do thing 1
         self.scope ->  {   do thing 2
                        {   do thing 3

        Args:
            code (str): The code that will be represented
        """
        self.code = code
        self.scope = scope if scope is not None else []
        self.whitespace = whitespace if whitespace else ' ' * 4
        self.line_ending = line_ending

    def add_child(self, child):
        """ Append a child to this statements scope 
        
        Args:
            child (Statement): The child to append
        """
        if isinstance(child, Statement):
            self.scope.append(child)
        else:
            raise Exception("child " + child + " is not a Statement")

    def add_children(self, child_list):
        """ A convenience function to load multiple children into this scope

        Args:
            child_list (list): a list of children to append to this objects scope
        """
        for child in child_list:
            self.add_child(child)

    def create_lineage(self, lineage):
        """ Create a hierarchical lineage of children with this object as the oldest member. eg.
        children = [c1, c2, c3]
        result -- self (top level)
                    |-> c1
                        |-> c2
                            |-> c3
        """
        current_node = self
        for child in lineage:
            current_node.add_child(child)
            current_node = child

    def from_parent(self, parent):
        """ Append this statement to a parents scope 
        
        Args:
            parent (Statement): The aprrent to be appended to
        """
        if isinstance(parent, Statement):
            parent.scope.append(self)
        else:
            raise Exception("parent " + parent + " is not a Statement")

    def from_lineage(self, lineage):
        """ Create a hierarchical list of parents with this object as the youngest decentant

        Lineage will be arranged in the order the parents are provided. eg.
        parents = [p1, p2, p3]
        result -- p1 (top level)
                  |->p2
                     |->p3
                        |->self
        In this example the top level parent would be at scope level n+1 and 
        this object would be at scope level n+4.

        Args:
            lineage (list): a hierarchical list of parents for this object.
        """
        current_node = self
        lineage.reverse()
        for parent in lineage:
            current_node.from_parent(parent)
            current_node = parent

    def format(self):
        """ Abstract function to format properties this object """
        pass

    def generate(self):
        """ Abstract function to set self.code """
        pass

    def build_renderer(self, *args, **kwargs):
        """ Overwrite this function to customize how render should be called
        for particular objects
        """
        return self.render(*args, **kwargs)

    def render(self, level=-1, increment=1):
        """ Return this statement and all children recursively 
        
        Args:
            level (int): The indentation level to set for this statement
            increment (int): The number of indentation levels for the child scope
        """
        yield "{}{}{}".format(self.whitespace * level, self.code,
                              self.line_ending)
        for child in self.scope:
            child.format()
            child.generate()
            child_renderer = child.build_renderer(level=level + increment)
            while 1:
                try:
                    yield child_renderer.next()
                except StopIteration:
                    break


class Document(Statement):
    """ All content is rooted in this base document """

    def __init__(self, *args, **kwargs):
        super(Document, self).__init__(*args, **kwargs)
        self.line_ending = ''

    def export(self):
        renderer = self.build_renderer()
        for node in renderer:
            yield node


def to_statement(item):
    if isinstance(item, basestring):
        val = Statement(item)
    elif isinstance(item, Statement):
        pass
    else:
        item = Statement()
    return item
