class Plugboard:
    """
    Plugboard: contains all the pluglead configurations for a specific enigma machine.
    """

    MAX_LEADS = 10

    def __init__(self):
        """
        Constructor.
        """
        self.leads = []


    def add(self, lead):
        """
        Adds a lead to the plugboard.
       
        Parameters:
            lead: the lead to add to the plugboard (PlugLead)
        Returns: None
        """

        # if we try to add something that isn't a plug lead
        if not isinstance(lead, PlugLead):
            raise TypeError("You can only add plug leads to the plugboard.")
        # if we are trying to add a plug lead to a full plugboard
        if len(self.leads) == Plugboard.MAX_LEADS:
            raise ValueError("Cannot add any more leads to the plugboard.")

        self.leads.append(lead)


    def encode(self, character):
        """
        Encodes a character if one of the leads connects it to another character.

        Parameters:
            character: the character to encode (str)
        Returns:
            the encoded character (str)
        """
        if not isinstance(character, str):
            raise TypeError("Character must be a string.")
        if len(character) != 1:
            raise ValueError("Character must be a single character.")

        for lead in self.leads:
            if character in lead.mapping_dict.keys():
                return lead.mapping_dict[character]

        return character
