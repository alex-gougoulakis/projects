class Rotor:
    """
    Defines:
    - the configuration of an enigma machine rotor
    - the functions needed to encode characters (R-->L, L-->R) using the rotor
    """

    # dictionary of 10 possible wirings and their notches
    # each key corresponds to a tuple (wiring, notch)
    # or each wiring, the nth element of the list corresponds to the nth letter of the english alphabet
    _POSSIBLE_ROTORS = {
        0: (['L', 'E', 'Y', 'J', 'V', 'C', 'N', 'I', 'X', 'W', 'P', 'B', 'Q', 'M', 'D', 'R', 'T', 'A', 'K', 'Z', 'G', 'F', 'U', 'H', 'O', 'S'], None),
        1: (['F', 'S', 'O', 'K', 'A', 'N', 'U', 'E', 'R', 'H', 'M', 'B', 'T', 'I', 'Y', 'C', 'W', 'L', 'Q', 'P', 'Z', 'X', 'V', 'G', 'J', 'D'], None),
        2: (['E', 'K', 'M', 'F', 'L', 'G', 'D', 'Q', 'V', 'Z', 'N', 'T', 'O', 'W', 'Y', 'H', 'X', 'U', 'S', 'P', 'A', 'I', 'B', 'R', 'C', 'J'], 'Q'),
        3: (['A', 'J', 'D', 'K', 'S', 'I', 'R', 'U', 'X', 'B', 'L', 'H', 'W', 'T', 'M', 'C', 'Q', 'G', 'Z', 'N', 'P', 'Y', 'F', 'V', 'O', 'E'], 'E'),
        4: (['B', 'D', 'F', 'H', 'J', 'L', 'C', 'P', 'R', 'T', 'X', 'V', 'Z', 'N', 'Y', 'E', 'I', 'W', 'G', 'A', 'K', 'M', 'U', 'S', 'Q', 'O'], 'V'),
        5: (['E', 'S', 'O', 'V', 'P', 'Z', 'J', 'A', 'Y', 'Q', 'U', 'I', 'R', 'H', 'X', 'L', 'N', 'F', 'T', 'G', 'K', 'D', 'C', 'M', 'W', 'B'], 'J'),
        6: (['V', 'Z', 'B', 'R', 'G', 'I', 'T', 'Y', 'U', 'P', 'S', 'D', 'N', 'H', 'L', 'X', 'A', 'W', 'M', 'J', 'Q', 'O', 'F', 'E', 'C', 'K'], 'Z'),
        7: (['E', 'J', 'M', 'Z', 'A', 'L', 'Y', 'X', 'V', 'B', 'W', 'F', 'C', 'R', 'Q', 'U', 'O', 'N', 'T', 'S', 'P', 'I', 'K', 'H', 'G', 'D'], None),
        8: (['Y', 'R', 'U', 'H', 'Q', 'S', 'L', 'D', 'P', 'X', 'N', 'G', 'O', 'K', 'M', 'I', 'E', 'B', 'F', 'Z', 'C', 'W', 'V', 'J', 'A', 'T'], None),
        9: (['F', 'V', 'P', 'J', 'I', 'A', 'O', 'Y', 'E', 'D', 'R', 'Z', 'X', 'W', 'G', 'C', 'T', 'K', 'U', 'Q', 'S', 'B', 'N', 'M', 'H', 'L'], None)
    }

    def __init__(self, wiring):
        """
        Constructor.

        Parameters:
            wiring: key corresponding to a value in the _POSSIBLE_ROTORS dictionary (int)
        """
        if not(isinstance(wiring, int)):
            raise TypeError("Wiring must be an integer.")

        self.wiring = copy.deepcopy(self._POSSIBLE_ROTORS[wiring][0])
        self.notch = self._POSSIBLE_ROTORS[wiring][1]

        # default values
        self.initial_position = 'A'
        self.ring_setting = 0
        self.position = 0
        self.turns_until_notch = 0
   

    # METHODS TO CONFIGURE ROTOR OBJECTS

    def set_initial_position(self, initial_position):
        """
        Sets the initial position of the rotor.

        Parameters:
            initial_position: the initial position (str, A-Z)
        Returns: None
        """
        if not isinstance(initial_position, str):
            raise TypeError("Initial position must be a string.")
        if len(initial_position) != 1:
            raise ValueError("Initial position must be a single character.")
        if not 65 <= ord(initial_position) <= 90:
            raise ValueError("Invalid initial position.")

        # the initial position of the rotor in terms of alphabetical index
        self.initial_position = ord(initial_position) % 65


    def set_ring_setting(self, ring_setting):
        """
        Sets the ring setting of the rotor.

        Parameters:
            ring_setting: the ring setting (str)
        Returns: None
        """
        if not isinstance(ring_setting, str):
            raise TypeError("Ring setting must be a string.")
        try:
            int(ring_setting)
        except ValueError:
            raise ValueError("Ring setting string must contain a number (01-26).")
        if not 1 <= int(ring_setting) <= 26:
            raise ValueError("Invalid ring setting.")

        # the ring setting of the rotor (we subtract 1 so it starts at 0, like the initial position)
        self.ring_setting = int(ring_setting) - 1


    def set_position(self):
        """
        Calculates and sets the final starting position of the rotor.

        Returns: None
        """
        # the final starting position, a combination of the initial position and the ring setting,
        # which have opposite offset effects
        position = self.initial_position - self.ring_setting
        if position > 0:
            self.position = position
        else:
            # count down from the end if it wraps around
            self.position = 26 + position


    def set_turns_until_notch(self):
        """
        Calculates and sets the number of turns until a rotor reaches its notch.

        Returns: None
        """  
        if self.has_notch():
            # the position of the notch in the alphabet
            notch_index = ord(self.notch) % 65

            # if we start before the notch
            if self.initial_position < notch_index:
                 self.turns_until_notch = notch_index - self.initial_position + 1
            # if we start after the notch
            else:
                self.turns_until_notch = (26 - self.initial_position) + notch_index + 1

        else:
            self.turns_until_notch = None

    # INSTANCE METHODS

    def encode_right_to_left(self, character, rotate=True):
        """
        Encodes a character from right to left.

        Parameters:
            character: the character to encode (str)
        Returns: the encoded character (str)
        """
        if not isinstance(character, str):
            raise TypeError("Character to be encoded must be a string.")
        if len(character) != 1:
            raise ValueError("Character to be encoded must be a single character.")

        if rotate:

            if self.has_notch():
                # one rotation closer to hitting the notch
                self.dec_turns_until_notch()
            # rotate rotor
            self.increase_position()
       
        # shift the input character <position> positions to the right in the alphabet
        shifted_char_pos = Rotor.shift_input(character, self.position)
        # get the character that corresponds to the shifted character in the rotor's wiring
        corresponding_char = self.wiring[shifted_char_pos]
        # shift the corresponding character <position> positions to the left in the alphabet
        shifted_output_pos = Rotor.shift_output(corresponding_char, self.position)
        # get the shifted character from its position
        shifted_output = Rotor.get_char_from_pos(shifted_output_pos)

        return shifted_output


    def encode_left_to_right(self, character):
        """
        Encodes a character from left to right.

        Parameters:
            character: the character to encode (str)
        Returns: the encoded character (str)
        """
        if not isinstance(character, str):
            raise TypeError("Character to be encoded must be a string.")
        if len(character) != 1:
            raise ValueError("Character to be encoded must be a single character.")

        # shift the input character <position> positions to the right in the alphabet
        shifted_char_pos = Rotor.shift_input(character, self.position)
        # get the character that corresponds to the shifted character in the rotor's wiring
        corresponding_char = Rotor.get_char_from_pos(self.wiring.index(Rotor.get_char_from_pos(shifted_char_pos)))
        # shift the corresponding character <position> positions to the left in the alphabet
        shifted_output_pos = Rotor.shift_output(corresponding_char, self.position)
        # get the shifted character from its position
        shifted_output = Rotor.get_char_from_pos(shifted_output_pos)
       
        return shifted_output


    def has_notch(self):
        """
        Returns whether or not the rotor has a notch. (bool)
        """
        return self.notch is not None

   
    def has_reached_notch(self):
        """
        Returns whether or not the rotor has reached the notch. (bool)
        """
        return self.has_notch() and self.turns_until_notch == 0


    def dec_turns_until_notch(self):
        """
        Decreases the amount of turns until the rotor hits its notch by 1.

        Returns: None
        """
        turns = self.turns_until_notch - 1
        if turns < 0:
            # reset
            self.turns_until_notch = 25
        else:
            self.turns_until_notch -= 1
   

    def increase_position(self):
        """
        Increases the rotor's current position by 1. If the current position becomes 26,
        the rotor's position is reset (position takes values 0-25).

        Returns: None
        """
        new_position = self.position + 1
        if new_position < 26:
            self.position = self.position + 1
        else:
            # reset
            self.position = 0


    # STATIC METHODS

    @staticmethod
    def shift_input(character, position):
        """
        Shifts a character to the right in the alphabet by <position> positions.
        If the shift takes it out of the alphabet's range (i.e. after Z),
        it wraps around and counts the remaining positions starting from A.

        Parameters:
            character: the character to be shifted (str)
            position: the number of positions to shift by (int)

        Returns: the index of the shifted character in the alphabet. (int)
        """
        if not isinstance(character, str):
            raise TypeError("Character to be shifted must be a string.")
        if len(character) != 1:
            raise TypeError("Character to be shifted must be a single character.")

        if ord(character) + position > 90:
            wraparound_char = 65 % (65 - (position - (90 - ord(character)) - 1))
            return wraparound_char
        else:
            # the character we reach if we shift <position> steps to the right
            shift = ord(character) + position
            # the position of the shifted character in the alphabet
            position = shift - 65
            return position


    @staticmethod
    def shift_output(character, position):
        """
        Shifts a character to the left in the alphabet by <position> positions.
        If the shift takes it out of the alphabet's range (i.e. before A),
        it wraps around and counts the remaining positions backwards starting from Z.

        Parameters:
            character: the character to be shifted (str)
            position: the number of positions to shift by (int)

        Returns: the index of the shifted character in the alphabet. (int)
        """
        if not isinstance(character, str):
            raise TypeError("Character to be shifted must be a string.")
        if len(character) != 1:
            raise TypeError("Character to be shifted must be a single character.")

        if ord(character) - position < 65:
            # the character reached if we shift <position> steps to the left
            full_shift = ord(character) - position
            # number of positions we have shifted to the left of A
            overshift = 65 - full_shift
            # the position of the final character when we wrap around
            wraparound_pos = 26 - overshift
            return wraparound_pos

        else:
            # the character we reach if we shift <position> steps to the left
            shift = ord(character) - position
            # the position of the shifted character in the alphabet
            position = shift - 65
            return position


    @staticmethod
    def get_char_from_pos(position):
        """
        Returns the character that corresponds to a certain position in the alphabet. (str)
        """
        if not isinstance(position, int):
            raise TypeError("Position must be an integer.")
        if not 0 <= position <= 25:
            raise IndexError("Position is out of bounds (0-25).")

        return chr(65 + position)


    # override __str__
    def __str__(self):
        """
        Returns a human-readable representation of a rotor. (str)
        """
        return f"""Wiring: {self.wiring}\n
                   Notch: {self.notch}\n
                   Ring Setting: {self.ring_setting}\n
                   Position: {self.position}\n
                   Turns until notch: {self.turns_until_notch}"""