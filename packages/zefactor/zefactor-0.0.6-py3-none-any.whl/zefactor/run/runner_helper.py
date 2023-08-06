import logging
import os
from zefactor.api.finder_core import FinderRefactor
from zefactor.api.replacer_core import ReplacerRefactor
from zefactor.api.entries import Entries
from zind.api.core_find import Find

class RunnerHelper:

  def __init__(self):
    pass

  def find_rename_candidates(self, loader):

    find_tokens = loader.get_find_tokens()
    replace_tokens = loader.get_replace_tokens()

    find = Find()
    file_matches = find.find(loader.get_cwd(), [])

    finder_refactor = FinderRefactor(suppress_warnings=True)
    replacer_refactor = ReplacerRefactor()

    rename_map = {}

    for file_match in file_matches:
      find_token_matches = finder_refactor.scan_text(file_match, find_tokens)
      replacement_map = {}
      for find_token_match in find_token_matches:
        replacement_text = finder_refactor.compute_replacement(find_token_match, find_tokens, replace_tokens)
        replacement_map[find_token_match] = replacement_text

      new_name = replacer_refactor.apply_text(file_match, replacement_map)
      if(len(new_name) > 0):
        rename_map[file_match] = new_name

    return rename_map

  def compute_refactor(self, loader):

    find_tokens = loader.get_find_tokens()
    replace_tokens = loader.get_replace_tokens()

    file_filter_tokens = loader.get_file_filter_tokens()
    for file_filter_token in file_filter_tokens:
      logging.debug("File filter token: " + str(file_filter_token))

    find = Find()
    file_matches = find.find(loader.get_cwd(), file_filter_tokens)

    entries = Entries()
    finder_refactor = FinderRefactor(suppress_warnings=True)
    for file_match in file_matches:
      logging.info("Found file: " + file_match)

      if not file_match.endswith('/'):
        find_token_matches = finder_refactor.scan_file(file_match, find_tokens)
        for find_token_match in find_token_matches:
          replacement_text = finder_refactor.compute_replacement(find_token_match, find_tokens, replace_tokens)
          entries.add_entry(file_match, find_token_match, replacement_text)

    return entries

  def apply_replacement(self, entries):
    replacer_refactor = ReplacerRefactor()
    all_replacements_map = entries.get_replacement_mappings()
    file_mapping = entries.get_file_mapping()

    for filepath in file_mapping:
      replacement_map = {}
      for find_text in file_mapping[filepath]:
        replacement_map[find_text] = all_replacements_map[find_text]

      self._generate_backup(filepath)
      replacer_refactor.apply(filepath, replacement_map)

  def _generate_backup(self, filepath):
    backup_dir = os.path.dirname(filepath)
    backup_filepath = backup_dir + os.path.sep + os.path.basename(filepath) + ".rr.backup"

    os.rename(filepath, backup_filepath)

    return backup_filepath

  def cleanup_backup(self, entries):
    file_mapping = entries.get_file_mapping()
    
    for filepath in file_mapping:
      backup_dir = os.path.dirname(filepath)
      backup_filepath = backup_dir + os.path.sep + os.path.basename(filepath) + ".rr.backup"
      os.remove(backup_filepath)

  def revert_backup(self, entries):
    file_mapping = entries.get_file_mapping()

    for filepath in file_mapping:
      backup_dir = os.path.dirname(filepath)
      backup_filepath = backup_dir + os.path.sep + os.path.basename(filepath) + ".rr.backup"
      os.rename(backup_filepath, filepath)
