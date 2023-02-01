# pull from xorshift.py file for randomization algorithm
import xorshift as xor

def find_index(ref_list: list, item) -> list:
    """
    List comprehension function that returns all indices of item appearance
    """
    return [index for index, value in enumerate(ref_list) if value == item]

class Note:
  """
  Class that defines the attributes and available modifactions specific to musical 
  notes. Takes as arguments (`note name: str, pitch: float, octave: int`)
  --------------------------

  ## Methods:

  - `getpitch():` return the pitch attribute of a Note() object

  - `pitchconv(semitone: int):` takes an integer value for the amount of semitones
  by which a `Note()` object should be translated by. Note name and octave are updated 
  accordingly and method returns f-string with combine note name and octave as well as
  the float value of the new pitch shifted frequency.

  """
  def __init__(self, name: str, pitch: float, octave: int) -> None:
    self.name = name
    self.pitch = pitch
    self.octave = octave
    self.note_names = ["C", "C♯", "D", 
                      "D♯", "E", "F", 
                      "F♯", "G", "G♯",
                      "A", "A♯", "B"]
    self.name_index = find_index(self.note_names, self.name)

  def getpitch(self):
    """
    Method to return the pitch of a `Note()` object as a `float`.
    """
    return self.pitch

  def pitch_conv(self, semi: int) -> float:
    """
    Method to change the pitch and subsequently the name / octave pair of a 
    `Note()` object. Takes an integer as an argument that is the amount of 
    semitones to shift the note by.
    """

    # Equal temperament calculation for interval from semitone
    temp_pitch = self.pitch * 2**(semi / 12)
    temp_index = (self.name_index[0] + semi) % 12
    temp_name = self.note_names[temp_index]

    up_crossing = len(self.note_names) - self.name_index[0]
    down_crossing = int(self.name_index[0] + 1)

    # Adjust the octave nomenclature if we have wrapped around the list either way
    # for shifts lesser than 12 semitones
    if semi > 0 and semi >= up_crossing:
      temp_octave = self.octave + 1 + ((semi - up_crossing) // 12)

    elif semi < 0 and abs(semi) >= down_crossing:
      temp_octave = self.octave - 1 - ((abs(semi) - down_crossing) // 12)

    else:
      temp_octave = self.octave

    return f"{temp_name}{temp_octave}", temp_pitch

  # Print method
  def __str__(self) -> str:
    return f"{self.name}{self.octave} :: {self.pitch}"


class Scale:
  """
  Class that defines the attributes and available modifactions 
  specific to musical scales built off of the Note() class.
  Takes as arguments (`scale name: str, base note: Note(), shift steps: list`)
  ---

  ## Methods:

  - `select_notes(note indices: list):` Return the note names and values of keys at a designated 
  index in the list of all keys from the dictionary of notes

  - `rand_select(i: int):` Return a number `i` of note names and values, randomly selected
  from the dictionary of notes

  - `getfreqaslist():` Return all the frequency values stored in our dictionary of notes
  as a list.

  - `getnotebyfreq(frequency: float):` Return the name of a note if the input frequency is 
  exactly in the values of our scaled note list.

  """
  def __init__(self, name: str, note: Note, steps: list) -> None:
    self.name = name
    self.note = note
    self.steps = steps
    self.members = {}
    prev_inst = 0
    pitch = self.note.getpitch()

    # Reversed list of steps for walking down
    back_calc = self.steps[::-1]
    
    # Create and store to a dictionary the whole range of auditory frequencies 
    # from the base note attributes.
    while pitch < 20000:
      for i in range(len(self.steps)):
        prev_inst += self.steps[i]
        marker, pitch = self.note.pitch_conv(prev_inst)
        self.members[marker] = pitch
      
    # Reset variable for second instance of walk
    prev_inst = 0
      
    while pitch > 20:
      for i in range(0, len(self.steps)):
        prev_inst -= back_calc[i]
        marker, pitch = self.note.pitch_conv(prev_inst)
        self.members[marker] = pitch

    # Store all keys from self.members as an indexable list
    self.note_names = [*self.members]

  def select_notes(self, note_choice: list) -> list:
    """
    Method to select specific notes from a scale and return them as a list.\n
    Takes as input: (`selection of notes: list`)
    """
    self.selection = {}

    # Can handle values greater than the length of the dictionary of notes by
    # wrapping values back around with modulo operator
    for i in range(len(note_choice)):
      key_pull = self.note_names[note_choice[i] % (len(self.members))]
      self.selection.update({key_pull: self.members[key_pull]})

    return self.selection

  def rand_select(self, count: int, return_type = "all") -> list:
    """
    Method to select a given amount of random notes from a scale and return them as a list.\n
    Takes as input: (`number of notes: int, type of return: str`)\n
    `type of return` can have the values: `"all"`, `"names"`, or `"pitches"`. If none are explicited 
    defaults to `"all"`
    """
    index_list = []

    # Add random note to list for (i <= count)
    for i in range(count):
      prng = xor.arbitrary(0, len(self.members) - 1)
      index_list.append(prng)

    self.selection = self.select_notes(index_list)
    
    # Determine what to return based off of the value of (return_type)
    if return_type == "all":
      return self.selection
    
    elif return_type == "names":
      return [*self.selection]
    
    elif return_type == "pitches":
      return list(self.selection.values())
    
  def getfreqaslist(self):
    """
    Return as a list all of the frequencies in our dictionary of notes.
    """
    return self.members.values()
  
  def getnotebyfreq(self, freq: float):
    """
    Return the name of a note if the input frequency is exactly in the values of our
    scaled note list. \n
    Takes as an argument: (`frequency: float`)
    """
    try:
      return list(self.members.keys())[list(self.members.values()).index(freq)]

    except ValueError:
      return f"{freq} is not in the scale"

  def __str__(self) -> str:
    """
    Print method for the `Scale()` object
    """
    return f"{self.name} :: {self.members}"