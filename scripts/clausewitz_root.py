from clausewitz_object import ClausewitzObject

class ClausewitzRoot(ClausewitzObject):
    def __init__(self, name):
        ClausewitzObject.__init__(self)
        self.name = name
