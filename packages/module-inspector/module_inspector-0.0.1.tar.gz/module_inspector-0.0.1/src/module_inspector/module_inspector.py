"""This module contains methods for other module's visualization."""

from string import ascii_letters


class Display:
    """Main module attributes display class."""
    def __init__(self, module, include_dunders_and_private=False):
        # Dictionary keys definition:
        if include_dunders_and_private:
            self.keys = '_' + ascii_letters
            self.attributes = sorted(module.__dir__())
        else:
            self.keys = ascii_letters
            self.attributes = [
                attribute for attribute in module.__dir__()
                if not attribute.startswith('_')
                ]

        # Entry assignment and empty instances removal:
        self.ordered_attributes = {char.upper(): [] for char in self.keys}
        for char in self.keys:
            self.ordered_attributes[char.upper()].extend([
                attribute for attribute in self.attributes
                if attribute.startswith(char)
                ])
        self.ordered_attributes = {
            key: value for key, value in self.ordered_attributes.items()
            if value != []
            }

        # Longest string determination:
        self.max = max([
            (len(attribute), attribute) for attribute in self.attributes
            ])

    def __repr__(self):
        out = '-' * (self.max[0] + 4) + '|\n'
        for key, values in self.ordered_attributes.items():
            # The '4' value compensates for the space taken up by decorations:
            out += f'# {key}'.ljust(self.max[0] + 4) + '|\n'
            for value in values:
                out += f'-> {value}'.ljust(self.max[0] + 4) + '|\n'
            out += '-' * (self.max[0] + 4) + '|\n'
        return out
