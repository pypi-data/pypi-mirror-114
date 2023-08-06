class Place:
  def __init__(self, place_doc):
    self.id = place_doc.attrib['id']
    self.text = place_doc.find('text').text
    self.type = place_doc.find('type').find('text').text
    self.__initmark = place_doc.find('initmark').find('text').text

  def __repr__(self):
    return f'<Place(id={self.id}, text={self.text}, type={self.type}, tokens={self.tokens})>'

  def __str__(self):
    return str(self.__dict__)

  def __eq__(self, other):
    if not isinstance(other, Place):
        return False
    return self.id == other.id

  def __hash__(self):
      return hash(self.id)


  @property
  def tokens(self):
    if self.__initmark is None:
      return

    if self.type == 'UNIT':
      token = self.__initmark.replace('`()','')
      return int(token)
    else:
      tokens = []
      for text in self.__initmark.replace('\n','').split('++'):
        token = text.split('`')
        tokens += [token[1]] * int(token[0])

      return tokens