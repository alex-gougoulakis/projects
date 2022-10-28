class PlugLead:
    """
    Pluglead: maps two different characters to each other.
    """

    def __init__(self, mapping):
        """
        Pluglead constructor.

        Parameters:
            mapping: two characters that will be mapped to each other (str)
        """
        if not isinstance(mapping, str):
            raise TypeError("Mapping must be a string.")
        if len(mapping) != 2:
            raise ValueError("Mapping must be comprised of two characters")

        if mapping[0] == mapping[1]:
            raise ValueError("You cannot map a character to itself.")

        # map the two characters to each other (both ways)
        self.mapping_dict = {mapping[0]: mapping[1],
                           mapping[1]: mapping[0]}


    def encode(self, character):
        """
        Encodes a character.

        Parameters:
            character: the character to be encoded (str)
       
        Returns: if character not in mapping dictionary: character itself (str)
                 otherwise: the char character is mapped to (str)
        """
        if not isinstance(character, str):
            raise TypeError("Character must be a string.")
        if not len(character) == 1:
            raise ValueError("Character must be a single character.")

        if character in self.mapping_dict.keys():
            return self.mapping_dict[character]

        # if the lead has no impact on the character
        return character
