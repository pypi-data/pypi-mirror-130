from io import StringIO
from zefactor.api.find_scanner import FindScanner
from zefactor.api.transform import Transform

class FinderRefactor:

  def __init__(self, suppress_warnings=False):
    self._suppress_warnings = suppress_warnings

  def scan_text(self, text, find_tokens):
    input_fd = StringIO(text)
    for item in self._scan(input_fd, find_tokens):
      yield item

  def scan_file(self, filepath, find_tokens):
    try:
      first_char = True
      with open(filepath, "r") as input_fd:
        for item in self._scan(input_fd, find_tokens):
          yield item
    except UnicodeDecodeError:
      if(not self._suppress_warnings):
        print("[WARNING] could not decode: " + filepath + " as utf-8, skipping refactor.")

  # Scans files and finds flexible matching patterns to the search tokens.
  def _scan(self, input_fd, find_tokens):

    find_scanners = []
    first_char = True

    while True:
      find_scanner = FindScanner(find_tokens)
      find_scanners.append(find_scanner)

      char = input_fd.read(1)
      if not char:
        break

      # A token must match a non-alphanumeric character to start the sequence
      # Except for the very first token in a file, so it should be seeded with a fake input.
      if(first_char):
        find_scanners[0].check_next("")
        first_char = False

      matched_find_scanners = []
      for find_scanner in find_scanners:
        match = find_scanner.check_next(char)
        if(match):
          if(find_scanner.is_done()):
            yield find_scanner.get_record()
          else:
            matched_find_scanners.append(find_scanner)
      find_scanners = matched_find_scanners
        
    # If the file terminates, add one empty string to all find_scanners
    for find_scanner in find_scanners:
      match = find_scanner.check_next("")
      if(find_scanner.is_done()):
        yield find_scanner.get_record()

  # Deterimines the case of a token given the prior casing and the next char
  # Cases are either 'upper', 'lower', 'title', or 'none' and if not set Python's None
  def resolve_case(self, current_case, next_char):
    if(current_case == "none"):
      return current_case

    if(current_case is None):
      if(next_char.isupper()):
        return "title"
      else:
        return "lower"
    else:
      if(next_char.isupper()):
        if(current_case == "title"):
          return "upper"
        elif(current_case == "lower"):
          return "none"
        return current_case
      else:
        if(current_case == "title" or current_case == "lower"):
          return current_case
        else:
          return "none"

  # Outputs a list of operations to apply to replace tokens
  def classify(self, raw_text, find_tokens):

    #print("AE:")
    #print(raw_text)
    #print(find_tokens)
    #print("AE-DONE")

    transform = Transform()

    case = None
    delimiter = ""

    find_tokens_index = 0
    char_index = 0

    first_raw = False
    for char in raw_text:

      if(first_raw):
        if(char.isalnum()):
          delimiter = ""
          transform.push(case, delimiter)
          if(char.isupper()):
            case = "title"
          else:
            case = "lower"
          char_index = char_index + 1
        else:
          delimiter = char
          transform.push(case, delimiter)
          case = None
        # Reset default values
        delimiter = ""
        first_raw = False
        continue


      case = self.resolve_case(case, char)
      
      if(char.lower() != find_tokens[find_tokens_index][char_index]):
        raise "Classification error"

      char_index = char_index + 1
      first_raw = False

      if(char_index == len(find_tokens[find_tokens_index])):
        find_tokens_index = find_tokens_index + 1
        char_index = 0
        first_raw = True

    # The last token always has a null delimiter.
    delimiter = ""
    transform.push(case, delimiter)

    return transform

  #def transform_replacement(self, transform, replace_tokens):
  #  pass

  # Computes replacements for the search tokens attempting to follow similar casing and stylistic rules
  def compute_replacement(self, raw_text, find_tokens, replace_tokens):
  
    transform = self.classify(raw_text, find_tokens)
    return transform.apply(replace_tokens)
