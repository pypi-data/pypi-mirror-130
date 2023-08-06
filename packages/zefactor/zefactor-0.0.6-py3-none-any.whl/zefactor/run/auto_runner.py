import sys
import logging
from zefactor.api.rename.renamer_core import RenamerRefactor
from zompt.api.arrow_selection_prompt import ArrowSelectionPrompt
from zefactor.input.loader import Loader
from zefactor.api.entries import Entries
from zefactor.run.runner_helper import RunnerHelper

class AutoRunner:

  def __init__(self, loader):
    self._loader = loader
    self._runner_helper = RunnerHelper()

  def _run_refactor(self):

    entries = self._runner_helper.compute_refactor(self._loader)

    replacement_mapping = entries.get_replacement_mappings()
    edited_files = entries.get_files()

    if(len(edited_files) == 0):
      print("No changes detected.")
    else:

      print("The following files will be edited (preview): ")
      for i in range(0, len(edited_files)):
        if(i > 7):
          print("...")
          break

        print(edited_files[i])

      print()
      print("The following replacements are planned:")
      for find_text in replacement_mapping:
        replacement_text = replacement_mapping[find_text]
        print("    " + find_text + "  ->  " + replacement_text)

      print()

      apply_replacements = "yes"
      if(not self._loader.is_auto_confirm()):
        print("Apply changes? (use arrow keys to select)")
        print()
        apply_prompt = ArrowSelectionPrompt(["yes","no"])
        apply_replacements = apply_prompt.run()
        print()

      print()
      if(apply_replacements == "yes"):
        self._runner_helper.apply_replacement(entries)
        print("Changes complete")
        print()

        print("Finalize Changes? (use arrow keys to select)")
        print()
        cleanup_prompt = ArrowSelectionPrompt(["yes - delete backup files", "yes - keep backup files", "no - revert changes"])
        cleanup_action = cleanup_prompt.run()
        print()
        print()
        if(cleanup_action == "yes - delete backup files"):
          self._runner_helper.cleanup_backup(entries)
          print("Backup files removed.")
        elif(cleanup_action == "yes - keep backup files"):
          print("Backup files retained.")
        elif(cleanup_action == "no - revert changes"):
          self._runner_helper.revert_backup(entries)
          print("Files reverted.")

  def _run_rename(self):

    rename_map = self._runner_helper.find_rename_candidates(self._loader)
    #for file_match in rename_map:
    #  print(file_match + " -> " + rename_map[file_match])
    renamer_refactor = RenamerRefactor()
    rename_operations = list(renamer_refactor.calculate(rename_map))

    if(len(rename_operations) > 0):
      print("The following file rename operations will be applied in order:")
      print()
      index = 1
      for name, rename in rename_operations:
        print(str(index) + ": " + name + " -> " + rename)
        index = index + 1
      print()

      print("Apply rename operations?")
      print()
      rename_prompt = ArrowSelectionPrompt(["yes", "no"])
      rename_action = rename_prompt.run()
      print()
      if(rename_action == "yes"):
        renamer_refactor.apply(rename_operations)
        print()
        print("File renames complete!")
    else:
      print("No file renames found.")

  def run(self):

    try:

      find_tokens = self._loader.get_find_tokens()
      replace_tokens = self._loader.get_replace_tokens()

      if(len(find_tokens) == 0):
        print("Missing required argument '-f'")
        return False
      if(len(replace_tokens) == 0):
        print("Missing required argument '-r'")
        return False

      if(not self._loader.is_skip_refactor()):
        self._run_refactor()

      if(not self._loader.is_skip_rename()):
        self._run_rename()

    except KeyboardInterrupt:
      pass

    print()
    print("Bye!")
