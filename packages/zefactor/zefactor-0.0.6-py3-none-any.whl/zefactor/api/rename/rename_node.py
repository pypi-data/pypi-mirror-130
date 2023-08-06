import json

class RenameNode:

  def __init__(self, name, rename):
    self._name = name
    self._rename = rename
    self._children = []

  def add_child(self, node):
    self._children.append(node)

  def get_name(self):
    return self._name

  def get_rename(self):
    return self._rename

  def get_children(self):
    return self._children

  def set_rename(self, rename):
    self._rename = rename

  def contains(self, name):
    for child in self._children:
      if(child.get_name() == name):
        return True

    return False

  def get_child(self, name):
    for child in self._children:
      if(child.get_name() == name):
        return child

  def __str__(self):
    obj = {}
    obj["/rename"] = self._rename
    for child in self._children:
      obj[child.get_name()] = json.loads(str(child))

    return json.dumps(obj)
