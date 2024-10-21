from clausewitz_object import ClausewitzObject

class ClausewitzRoot(ClausewitzObject):
    def __init__(self, name_values:'dict[str, list]|None'=None, anonymous_values:'list|None'=None) -> None:
        ClausewitzObject.__init__(self, name_values=name_values, anonymous_values=anonymous_values)

    def unparse(self, separator='\t') -> str:
        anonymous_objects: str = ''
        anonymous_values: str = ''
        for element in self.anonymous_values:
            if isinstance(element, ClausewitzObject):
                anonymous_objects = f'{anonymous_objects}{element.unparse(depth=1, separator=separator)}\n'
            else:
                anonymous_values = f'{anonymous_values}{element} '
        
        named_values: str = ''
        for name, values in self.name_values.items():
            for element in values:
                if isinstance(element, ClausewitzObject):
                    named_values = f'{named_values}{name} = {element.unparse(depth=1, separator=separator)}\n'
                else:
                    named_values = f'{named_values}{name} = {element}\n'
            pass

        final_form:str = f'{anonymous_objects}{anonymous_values}\n{named_values}'.strip()
        return final_form

    def write(self, path: str):
        with open(path, 'w', encoding='utf-8-sig') as file:
            file.write(self.unparse())