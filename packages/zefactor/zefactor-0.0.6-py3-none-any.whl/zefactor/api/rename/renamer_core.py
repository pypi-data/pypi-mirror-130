from zefactor.api.rename.rename_node import RenameNode
import os

class RenamerRefactor:

  def __init__(self):
    pass

  # Generate a tree with the following structure:
  # name
  # rename
  # children
  def _generate_rename_tree(self, rename_map):

    root = RenameNode("", "")

    for name in rename_map:
      rename = rename_map[name]
      node = root

      name_parts = name.split('/')
      rename_parts = rename.split('/')
      rename_index = 0
      for name_part in name_parts:

        rename_part = None
        if(rename_index < len(rename_parts)):
          rename_part = rename_parts[rename_index]

        if(not node.contains(name_part)):
          child = RenameNode(name_part, rename_part)
          node.add_child(child)

        node = node.get_child(name_part)
        # It's possible for a node to be created by an earlier step without being renamed.
        if(node.get_rename() == node.get_name()):
          node.set_rename(rename_part)
          
        rename_index = rename_index + 1

    return root

  def _generate_rename_operations(self, pairs):

    index = 0
    while(index < len(pairs)):

      base_path, node = pairs[index]

      name = node.get_name()
      rename = node.get_rename()

      full_name = base_path + "/" + name
      if(base_path == ""):
        full_name = name

      full_rename = full_name
     
      if(name != rename):
        full_rename = base_path + "/" + str(rename)
        if(base_path == ""):
          full_rename = str(rename)
        yield (full_name, full_rename)

      for child in node.get_children():
        pairs.append((full_rename, child))

      index = index + 1

  def calculate(self, rename_map):
    rename_tree = self._generate_rename_tree(rename_map)
    return self._generate_rename_operations([("",rename_tree)])

  def apply(self, rename_operations):
   for name, rename in rename_operations:
     os.rename(name, rename)
