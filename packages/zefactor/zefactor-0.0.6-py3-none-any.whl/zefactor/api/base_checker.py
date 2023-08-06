class BaseChecker:

  # Given a list of tokens like [ happy, turtle ]
  # It will check against a stream of characters to see if they match
  # This assumes there will be a placeholder between the tokens
  def __init__(self, check_strings):
    self._check_strings = []
    self._check_strings.extend(check_strings)
    self._check_string = self._check_strings.pop(0)
    self._index = 0

    # In order to fully match, the token must terminate with a non-alphanumeric char. This is so 'rock' won't match tokens like 'rocket'.
    self._started = True
    self._matched = False
    self._done = False

  def check_next(self, next_char):

    # A match must start with a non-alphanumeric character
    if(self._started):
      self._started = False
      if(next_char.isalnum()):
        return False
      else:
        return True

    # If we are done matching, the next character must terminate the sequence by being non-alphanumeric
    if(self._matched):
      if(not next_char.isalnum()):
        self._done = True
        return True
      else:
        return False

    # When checking the next character between tokens, any non-alphanumeric is allowed 
    # or the first character in the next token must be present
    if(self._index == -1):
      if(not next_char.isalnum()):
        self._index = 0
        return True
      elif(next_char == self._check_string[0]):
        self._index = 1
        return True
      else:
        return False

    if(self._check_string[self._index] == next_char):

      # Check next index
      self._index = self._index + 1
      if(self._index == len(self._check_string)):
        if(len(self._check_strings) > 0):
          self._check_string = self._check_strings.pop(0)
          self._index = -1
        else:
          self._matched = True

      return True
    else:
      return False

  def is_done(self):
    return self._done
