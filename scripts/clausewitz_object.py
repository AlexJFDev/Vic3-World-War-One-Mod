class ClausewitzObject:
    """An object used for working with Paradox modding files.
    Fundamentally, it is like a dictionary and a list. It allows for 'named values', which are stored in a dictionary and 'anonymous values' which are stored in a list.
    Furthermore, any number of values can be associated with a name instead of just one like a regular dictionary."""
    def __init__(self, name_values:'dict[str, list]|None'=None, anonymous_values:'list|None'=None) -> None:
        """Initialize a new ClausewitzObject. Optionally takes a dictionary in 'name_values' or a list in 'anonymous_values'."""
        self.name_values = name_values
        self.anonymous_values = anonymous_values
        if name_values is None:
            self.name_values: dict[str, list] = {}
        if anonymous_values is None:
            self.anonymous_values: list = []
    
    def add_named_value(self, name: str, value) -> None:
        """Add a named value. Takes a string for the name and a value."""
        previous_values = self.name_values.get(name, [])
        previous_values.append(value)
        self.name_values[name] = previous_values

    def get_value_named(self, name: str, index=0, default=None) -> 'str|int|ClausewitzObject|None':
        """Gets a single value assigned to `name`. Because multiple values can be assigned to a name, the `index` can be specified. Returns `default` or None if no values are assigned to name."""
        values = self.name_values.get(name, None)
        if values is None:
            return default
        if index > len(values) - 1:
            raise IndexError(f'The index {index} is greater than the number of values assigned to {name} ({len(values)}).')
        return values[index]
    
    def get_values_named(self, name: str, default=None) -> 'list[str|int|ClausewitzObject|None]':
        """Gets all values assigned to `name` in the form of a list. Returns `default` if no values are assigned to the name."""
        values = self.name_values.get(name, None)
        if values is None:
            return default
        return values
    
    def get_name_value_pairs(self) -> dict[str, list]:
        """Gets all name value pairs in the form of a dictionary. The name is the key and the value is a list of all values assigned to that name."""
        return self.name_values
    
    def get_names(self) -> list:
        """Returns a list containing all names in the object."""
        return self.name_values.keys()

    def add_anonymous_value(self, value) -> None:
        """Adds an anonymous value to the object."""
        self.anonymous_values.append(value)

    def add_anonymous_values(self, *values) -> None:
        """Adds any number of anonymous values to the object."""
        self.anonymous_values += values

    def join_anonymous_values(self, values) -> None:
        """Joins a list of anonymous values to the preexisting anonymous values."""
        self.anonymous_values += values
    
    def get_anonymous_values(self) -> list:
        """Gets the entire list of anonymous values."""
        return self.anonymous_values
    
    def pop_anonymous_values(self):
        """Pops the last anonymous value."""
        if len(self.anonymous_values == 0):
            raise IndexError('Cannot pop object with no anonymous values.')
        return self.anonymous_values.pop()
    
    def unparse(self, depth=0, separator='\t') -> str:
        """Generates a string, representing the object, that can be used in a Paradox mod."""
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
