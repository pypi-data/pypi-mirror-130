from zefactor.api.replace_scanner import ReplaceScanner
from zefactor.api.replace_semaphore import ReplaceSemaphore
import os
from io import StringIO

class ReplacerRefactor:

  def __init__(self):
    pass

  def apply_text(self, text, replacement_map):
    input_fd = StringIO(text)
    output_fd = StringIO()
    self._apply_replacements(input_fd, output_fd, replacement_map)
    return output_fd.getvalue()

  def _apply_replacements(self, input_fd, output_fd, replacement_map):

    replace_semaphore = ReplaceSemaphore()

    index = 0
    continue_loop = True
    while continue_loop:

     # if(index > 90):
     #   print("Exiting early")
     #   import sys
     #   sys.exit(0)

      # A token must match a non-alphanumeric character to start the sequence
      # Except for the very first token in a file, so it should be seeded with a fake input.
      char = None
      if(index == 0):
        char = ""
      else:
        char = input_fd.read(1)

      if index != 0 and not char:
        # Scan one more terminating character to represent file end.
        continue_loop = False
        char = ""

      replace_semaphore.register_char(index, char)

      for find_text in replacement_map:
        replace_text = replacement_map[find_text]
        base_replace_scanner = ReplaceScanner(find_text, replace_text, index, char)
        replace_semaphore.register_scanner(index, find_text, base_replace_scanner)


      ##print(replace_semaphore)

      done = False
      write_chars = ""
      for scanner_index, replace_scanner in replace_semaphore.get_scanners():
        match = replace_scanner.check_next(char)
        if(match):
          if(replace_scanner.is_done()):
            find_text = replace_scanner.get_find_text()
            replace_text = replace_scanner.get_replace_text()
            # If a match is done write out the replacement text
            output_fd.write(replace_scanner.get_start_symbol())
            output_fd.write(replace_text)
            replace_semaphore.mark_done(scanner_index, find_text, replace_text)
            done = True
        else:
          write_char = replace_semaphore.unregister_scanner(scanner_index, replace_scanner.get_find_text())
          if(len(write_char) > 0):
            write_chars = write_chars + write_char

      if(len(write_chars) > 0 and done is not True):
        output_fd.write(write_chars)

      index = index + 1

  def apply(self, filepath, replacement_map):

    backup_dir = os.path.dirname(filepath)
    backup_filepath = backup_dir + os.path.sep + os.path.basename(filepath) + ".rr.backup"

    with open(backup_filepath, "r") as input_fd:
      with open(filepath, "w") as output_fd:
        self._apply_replacements(input_fd, output_fd, replacement_map)
