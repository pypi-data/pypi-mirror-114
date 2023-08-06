class Transition:
  def __init__(self, trans_doc):
    self.id = trans_doc.attrib['id']
    self.text = trans_doc.find('text').text
    self._time = trans_doc.find('time').find('text').text

  def __repr__(self):
    return f'<Transition(id={self.id}, text={self.text}, time={self.time})>'

  def __str__(self):
    return str(self.__dict__)

  def __eq__(self, other):
    if not isinstance(other, Transition):
        return False
    return self.id == other.id

  def __hash__(self):
      return hash(self.id)

  @property
  def time(self):
    if self._time is None:
      return

    time = int(self._time.replace('@+',''))
    return time