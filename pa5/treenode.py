"""
CAPP 30121, Autumn 2026: Class for representing trees.
"""


class TreeNode:
    def __init__(self, code, label, weight):
        """
        Construct a Tree node

        Args:
            code: (string) a code that identifies the type of the node
            label: (string) a label that identifies the node
            weight: (float) an application specific weight
        """
        self.code = code
        self.label = label
        self.weight = weight
        self.__children = {}

    def get_children_as_dict(self):
        """
        Returns (Dict[str, TreeNode]): returns the children as a dictionary.
          This method should only be used by the utility functions that
          build the tree.  Student code should not use this method.
        """
        # Students...do not use this method.
        return self.__children

    def get_children_as_list(self):
        """
        Returns (List[TreeNode]): the children of the node as a list
        """
        return [self.__children[x] for x in sorted(self.__children)]

    def print_tree(self, tabs=""):
        """
        Print a tree

        Args:
            tabs (str): a string a spaces to use as a prefix for the each
              line in the output.
        """
        if self.code:
            code = self.code
            label = self.label
        else:
            code = 'Artificial root: code is "".'
            label = 'label is "".'
        s = "{}{} {} (weight: {:d})".format(tabs, code, label, self.weight)
        print(s)
        for key in sorted(self.__children):
            self.__children[key].print_tree(tabs + "    ")
