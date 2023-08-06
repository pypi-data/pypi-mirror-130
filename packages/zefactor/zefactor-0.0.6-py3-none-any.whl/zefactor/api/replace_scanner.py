from zefactor.api.base_checker import BaseChecker

class ReplaceScanner:

  def __init__(self, find_text, replace_text, index, start_symbol):
    self._checker = BaseChecker([ find_text ])

    self._find_text = find_text
    self._replace_text = replace_text
    self._index = index
    self._start_symbol = start_symbol

    self._is_done = False

  def get_find_text(self):
    return self._find_text

  def get_replace_text(self):
    return self._replace_text

  #def get_index(self):
  #  return self._index

  def get_start_symbol(self):
    return self._start_symbol

  def check_next(self, next_char):
    return self._checker.check_next(next_char)

  def is_done(self):
    return self._checker.is_done()
