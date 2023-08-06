from zefactor.api.base_checker import BaseChecker

class FindScanner:

  def __init__(self, check_strings):
    self._record_chars = []
    self._checker = BaseChecker(check_strings)

  def check_next(self, next_char):
    self._record_chars.append(next_char) # When finding matches, use flexible casing
    return self._checker.check_next(next_char.lower())

  def get_record(self):
    # Remove the terminating start and end characters
    return "".join(self._record_chars[1:-1])

  def is_done(self):
    return self._checker.is_done()
