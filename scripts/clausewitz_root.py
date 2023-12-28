from clausewitz_object import ClausewitzObject

class ClausewitzRoot(ClausewitzObject):
    def __init__(self, name):
        ClausewitzObject.__init__(self)
        self.name = name

    def unparse(self, separator='\t') -> str:
        return f'{self.name} = {ClausewitzObject.unparse(self, depth=1, separator=separator)}'
