class ClausewitzObject:
    def __init__(self) -> None:
        self.name_values: dict[str, list] = {}
        self.anonymous_values = []
    
    def add_named_value(self, name: str, value) -> None:
        previous_values = self.name_values.get(name, [])
        previous_values.append(value)
        self.name_values[name] = value

    def get_named_value(self, name, index=0):
        values = self.name_values.get(name, None)
        if values is None:
            raise KeyError(f'{name} has not been assigned any values.')
        if index > len(values) - 1:
            raise IndexError(f'The index {index} is greater than the number of values assigned to {name} ({len(values)}).')
        return values[index]
    
    def get_named_values(self, name) -> list:
        values = self.name_values.get(name, None)
        if values is None:
            raise KeyError(f'{name} has not been assigned any values.')
        return values

    def add_anonymous_value(self, value) -> None:
        self.anonymous_values.append(value)
    
    def get_anonymous_values(self) -> list:
        return self.anonymous_values
    
    def pop_anonymous_values(self):
        if len(self.anonymous_values == 0):
            raise IndexError('Cannot pop object with no anonymous values.')
        return self.anonymous_values.pop()