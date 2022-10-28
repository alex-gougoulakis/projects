import itertools
import string
import copy

# method which returns a Rotor object
# @param - name - name of the Rotor e.g. I or Gamma
def rotor_from_name(name):
    """
    Returns a rotor object with the corresponding wiring, given its name.

    Parameters:
        name: the name of the rotor (str)
    Returns: the corresponding rotor (Rotor)
    """
    # if the name is not a string
    if not isinstance(name, str):
        raise TypeError("The name of the rotor must be a string.")
   
   # mappings the different rotor names correspond to
    MAPPING = {
        "BETA": 0,
        "GAMMA": 1,
        "I": 2,
        "II": 3,
        "III": 4,
        "IV": 5,
        "V": 6,
        "A": 7,
        "B": 8,
        "C": 9    
    }
   
    # if the name does not correspond to a rotor
    if name.upper() not in MAPPING.keys():
        raise KeyError("There is no such rotor.")

    rotor_num = MAPPING[name.upper()]
    return Rotor(rotor_num)

   
class EnigmaMachine:
    """
    Defines:
        - a fully configureable enigma machine
        (rotors, reflector, ring settings, rotor positions, plugboard pairs)
        - methods that allow it to encode text
    """

    def __init__(self, rotors, reflector, ring_settings, initial_positions, plugboard_pairs=[]):
        """
        Constructor. Creates an enigma machine with the given characteristics.

        Parameters:
            rotors: rotors used in this enigma machine (str)
            reflector: reflector used in this enigma machine (str)
            ring_settings: ring settings for the rotors (str)
            initial_positions: starting positions of the rotors (str)
            plugboard_pairs: plugboard pairs to be used, default is an empty list (list)

        Parameter description credit goes to the author of the original enigma.ipynb.
        """
        # if the arguments are not all strings
        if not all(isinstance(arg, str) for arg in [rotors, ring_settings, initial_positions]):
            raise TypeError("Rotors, reflector, ring settings, and initial positions must be strings.")
       
        self.plugboard = Plugboard()
        self.rotors = []

        if isinstance(reflector, str):
            self.reflector = rotor_from_name(reflector)
        elif isinstance(reflector, Rotor):
            self.reflector = reflector
        else:
            raise TypeError("Reflector must be a string.")

        # separate rotors and their attributes
        rotors_list = rotors.split()
        ring_settings_list = ring_settings.split()
        initial_positions_list = initial_positions.split()

        # catch inconsistencies  
        if not (len(rotors_list) == len(ring_settings_list) == len(initial_positions_list)):
            raise ValueError("You have not provided a consistent number of rotors, ring settings, and initial positions.")
        if len(rotors_list) > 4:
            raise ValueError("You have provided too many rotors. The maximum is 4.")
        if len(rotors_list) < 3:
            raise ValueError("You have provided too few rotors. The minumum is 3.")

        # fill the rotor list with rotor objects
        self.initialize_rotors(rotors_list, ring_settings_list, initial_positions_list)
       
        if not isinstance(plugboard_pairs, list):
            raise TypeError("Plugboard pairs must be a list.")

        # add leads to the plugboard
        self.add_leads(plugboard_pairs)


    def encode(self, text):
        """
        Encodes text according to the configuration of the enigma machine.

        Parameters:
            text: the text to be encoded (str)
        Returns:
            the encoded text (str)
        """
        # in case non capital letters are given
        text = text.upper()
        result = ""
   
        for char in text:
            result += self.encode_single(char)

        return result
     

    def encode_single(self, char):
        """
        Encodes a single character according to the configuration of the enigma machine.

        Parameters:
            char: the character to be encoded (str)
        Returns: the encoded character (str)
        """
        result = self.run_through_leads(char)
        position = -1
        reversed_rotors = self.rotors[::-1]
       
        # send character through the rotors from right to left
        for rotor in reversed(self.rotors):
           
            position += 1

            # CONDITIONS FOR ROTATING
            # c1: the rotor is the 1st rotor, which always rotates
            # c2: the rotor is not the 4th rotor, which never rotates (if one exists)
            # c3: the rotor is either the 2nd or the 3rd rotor, which rotates only
            # if the previous rotor has a notch and has reached the notch

            c1 = rotor == self.rotors[-1]

            if len(self.rotors) == 4:
                # the rotor is not the 4th rotor
                c2 = rotor != self.rotors[0]
            else:
                # there is no 4th rotor
                c2 = True

            # 2nd/3rd rotor
            c3 = (not c1) and (c2) and (reversed_rotors[position - 1].has_reached_notch())

            rotate = c1 or c3
           
            result = rotor.encode_right_to_left(result, rotate=rotate)
           
        # send resulting character through the reflector
        result = self.reflector.encode_right_to_left(result, rotate=False)

        # send resulting character through the rotors from left to right
        for rotor in self.rotors:
            result = rotor.encode_left_to_right(result)

        result = self.run_through_leads(result)
       
        return result

    def run_through_leads(self, char):
        """
        Modifies the value of the character according to the machine's plugboard configuration.
        If the no pluglead is connected to the character, it remains the same.

        Parameters:
            char: the character to be modified (str)
        Returns: the modified (or not) character (str)
        """
        if not isinstance(char, str):
            raise TypeError("Character to pass through leads must be a string.")
        if len(char) != 1:
            raise ValueError("Character to pass through leads must be a single character.")

        result = char
        for lead in self.plugboard.leads:
            result = lead.encode(result)
        return result


    def add_leads(self, plugboard_pairs):
        """
        Add leads corresponding to chartacter pairs to the enigma machine's plugboard.

        Parameters:
            plugboard_pairs: the character pairs the leads will connect (list)
        Returns: None
        """
        for pair in plugboard_pairs:
            if not isinstance(pair, str):
                raise TypeError("Plugboard pairs must be strings.")
            if len(pair) != 2:
                raise ValueError("Plugboard pairs must be pairs of two characters.")

            pair = pair.upper()
            lead = PlugLead(pair)
            self.plugboard.add(lead)


    def initialize_rotors(self, rotors_list, ring_settings_list, initial_positions_list):
        """
        Initializes the enigma machine's rotors.

        Parameters:
            rotors_list: list of rotor names (list)
            ring_settings_list: list of ring settings (list)
            initial_positions_list: list of initial positions (list)
        Returns: None
        """
        for i in range(len(rotors_list)):
            # get and set each rotor's attributes
            rotor = rotor_from_name(rotors_list[i])
            rotor.set_initial_position(initial_positions_list[i])
            rotor.set_ring_setting(ring_settings_list[i])
            rotor.set_position()
            rotor.set_turns_until_notch()

            # add the rotor to the enigma machine
            self.rotors.append(rotor)



def swap_cross(reflector, pair):
    """
    Takes two pairs in a reflector and crosses their wires.
    Example: A --> E, B --> J becomes A --> J, B --> E

    Parameters:
        reflector: the reflector to be modified (Rotor)
        pair: the first two characters of each pair to be modified
              (for the example above, ('A', 'B')) (tuple)
    Returns: the reflector with its wires crossed (Rotor)
    """
    if not(isinstance(reflector, Rotor)):
        raise TypeError("Reflector must be a rotor.")
    if not(isinstance(pair, tuple)):
        raise TypeError("Pair must be a tuple.")
   
    # alphabetical index
    first_index = ord(pair[0]) % 65
    second_index = ord(pair[1]) % 65

    # index contents
    first_content = reflector.wiring[first_index]
    second_content = reflector.wiring[second_index]

    # replace the content of the first index with that of the second index
    # and vice versa
    # A --> B, C --> D: A --> D, B --> C
    reflector.wiring[first_index] = second_content
    reflector.wiring[second_index] = first_content

    # B --> A, D --> C: B --> C, D --> A
    first_other_index = ord(first_content) % 65
    second_other_index = ord(second_content) % 65

    reflector.wiring[first_other_index] = pair[1]
    reflector.wiring[second_other_index] = pair[0]
   
    return reflector


def swap_loop(reflector, pair):
    """
    Takes two pairs in a reflector and changes their wiring as such:
    Example: A --> E, B --> J becomes A --> B, E --> J

    Parameters:
        reflector: the reflector to be modified (Rotor)
        pair: the first two characters of each pair to be modified
              (for the example above, ('A', 'B')) (tuple)
    Returns: the reflector with its wiring changed (Rotor)
    """
    if not(isinstance(reflector, Rotor)):
        raise TypeError("Reflector must be a rotor.")
    if not(isinstance(pair, tuple)):
        raise TypeError("Pair must be a tuple.")

    # alphabetical index
    first_index = ord(pair[0]) % 65
    second_index = ord(pair[1]) % 65

    # index contents
    first_content = reflector.wiring[first_index]
    second_content = reflector.wiring[second_index]

    # A --> B, C --> D: A --> C, B --> D
    reflector.wiring[first_index] = pair[1]
    reflector.wiring[second_index] = pair[0]

    # B --> A, D --> C: B --> D, A --> C
    reflector.wiring[ord(first_content) % 65] = second_content
    reflector.wiring[ord(second_content) % 65] = first_content

    return reflector


def create_enigma_machine(rotors, reflector, ring_settings, initial_positions, plugboard_pairs):
    """
    Method that returns a configured enigma machine object. (EnigmaMachine)

    Parameters:
        rotors: rotors used in this enigma machine (str)
        reflector: reflector used in this enigma machine (str)
        ring_settings: ring settings for the rotors (str)
        initial_positions: starting positions of the rotors (str)
        plugboard_pairs: plugboard pairs to be used, default is an empty list (list)

    Parameter description credit goes to the author of the original enigma.ipynb.
    """
    enigma = EnigmaMachine(rotors, reflector, ring_settings, initial_positions, plugboard_pairs)
 
    return enigma
