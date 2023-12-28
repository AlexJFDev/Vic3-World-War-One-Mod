class ClausewitzObject:
    def __init__(self, name_values:dict[str, list]|None=None, anonymous_values:list|None=None) -> None:
        self.name_values = name_values
        self.anonymous_values = anonymous_values
        if name_values is None:
            self.name_values: dict[str, list] = {}
        if anonymous_values is None:
            self.anonymous_values: list = []
    
    def add_named_value(self, name: str, value) -> None:
        previous_values = self.name_values.get(name, [])
        previous_values.append(value)
        self.name_values[name] = previous_values

    def get_named_value(self, name: str, index=0):
        values = self.name_values.get(name, None)
        if values is None:
            raise KeyError(f'{name} has not been assigned any values.')
        if index > len(values) - 1:
            raise IndexError(f'The index {index} is greater than the number of values assigned to {name} ({len(values)}).')
        return values[index]
    
    def get_named_values(self, name: str) -> list:
        values = self.name_values.get(name, None)
        if values is None:
            raise KeyError(f'{name} has not been assigned any values.')
        return values

    def add_anonymous_value(self, value) -> None:
        self.anonymous_values.append(value)

    def add_anonymous_values(self, *values) -> None:
        self.anonymous_values += values

    def join_anonymous_values(self, values) -> None:
        self.anonymous_values += values
    
    def get_anonymous_values(self) -> list:
        return self.anonymous_values
    
    def pop_anonymous_values(self):
        if len(self.anonymous_values == 0):
            raise IndexError('Cannot pop object with no anonymous values.')
        return self.anonymous_values.pop()
    
    def unparse(self, depth=0, separator='\t') -> str:
        full_separator: str = separator * depth

        anonymous_objects: str = ''
        anonymous_values: str = ''
        for element in self.anonymous_values:
            if isinstance(element, ClausewitzObject):
                anonymous_objects = f'{anonymous_objects}\n{full_separator}{element.unparse(depth=depth + 1, separator=separator)}'
            else:
                anonymous_values = f'{anonymous_values}{element} '
        if anonymous_values:
            anonymous_values = f'\n{full_separator}{anonymous_values}'
        
        named_objects: str = ''
        named_values: str = ''
        for name, values in self.name_values.items():
            for element in values:
                if isinstance(element, ClausewitzObject):
                    named_objects = f'{named_objects}\n{full_separator}{name} = {element.unparse(depth=depth + 1, separator=separator)}'
                else:
                    named_values = f'{named_values}\n{full_separator}{name} = {element}'
            pass

        final_form:str = f'{"{"}{anonymous_objects}{anonymous_values}{named_objects}{named_values}\n{separator * (depth - 1)}{"}"}'
        return final_form
