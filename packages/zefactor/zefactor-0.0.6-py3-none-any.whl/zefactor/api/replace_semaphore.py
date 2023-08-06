class ReplaceSemaphore:

  def __init__(self):
    self._index_scanner = {}
    self._index_char = {}
    self._index_count = {}

  def register_char(self, index, char):
    self._index_char[index] = char

  def register_scanner(self, index, scanner_key, scanner):
    ##print("REGISTERING: " + str(index) + "-" + scanner_key)
    if(index not in self._index_scanner):
      self._index_scanner[index] = {}

    self._index_scanner[index][scanner_key] = scanner

    # Increase semaphore range by 1 because sequences must contain an extra terminating character
    for count in range(index, index + len(scanner_key) + 1):
      if(count not in self._index_count):
        self._index_count[count] = 1
      else:
        self._index_count[count] = self._index_count[count] + 1

  def get_scanners(self):
    scanner_list = []
    for index in self._index_scanner:
      for scanner_key in self._index_scanner[index]:
        scanner_list.append((index, self._index_scanner[index][scanner_key]))

    return scanner_list

  def unregister_scanner(self, index, scanner_key):

    ##print("UNREGISTERING: " + str(index) + "-" + scanner_key)
    char = ""

    self._index_scanner[index].pop(scanner_key)

    for count in range(index, index + len(scanner_key) + 1):
      self._index_count[count] = self._index_count[count] - 1
      if(self._index_count[count] == 0):

        if(count in self._index_char):
          char = char + self._index_char[count]

        self._index_char.pop(count, None)
        self._index_count.pop(count, None)
        self._index_scanner.pop(count,None)

    return char

  def mark_done(self, index, find_text, replace_text):
    ##print("MARK DONE ENTERED: " + str(index) + "-" + replace_text)
    for count in range(index, index + len(find_text)):
      if(count in self._index_scanner):
        for scanner_key in self._index_scanner[count]:
          for char_count in range(count, count + len(scanner_key)):
            self._index_count[char_count] = self._index_count[char_count] - 1
            if(self._index_count[char_count] == 0):
              # TODO: Possible bugs - there may be cases where the below is not the full story
              self._index_count.pop(char_count, None)
              self._index_char.pop(char_count, None)

      ##if(count in self._index_scanner):
      ##  for scanner_key in self._index_scanner[count]:
      ##    print("DONE REMOVING: " + str(count) + "-" + scanner_key)
      self._index_scanner.pop(count, None)

  def __str__(self):
    indexes = sorted(self._index_char.keys())

    content_list = []
    for index in indexes:
      char = self._index_char[index]
      count = self._index_count[index]
      content_list.append(str(count) + char)

    output_tokens = "tokens [ " + ", ".join(content_list) + " ]"

    output_scanners = ""
    for index, scanner in self.get_scanners():
      output_scanners = output_scanners + str(index) + "-" + scanner.get_find_text() + "\n"
      

    return output_tokens + "\n" + output_scanners
