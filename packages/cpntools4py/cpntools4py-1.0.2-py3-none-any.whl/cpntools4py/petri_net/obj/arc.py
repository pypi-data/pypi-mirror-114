class Arc:
  def __init__(self, arc_doc):
    self.id = arc_doc.attrib['id']
    self.orientation = arc_doc.attrib['orientation']
    self.placeend = arc_doc.find('placeend').attrib['idref']
    self.transend = arc_doc.find('transend').attrib['idref']


  def __repr__(self):
    return f'<Arc(id={self.id}, orientation={self.orientation}, placeend={self.placeend}, transend={self.transend})>'

  def __str__(self):
    return str(self.__dict__)

  def __eq__(self, other):
    if not isinstance(other, Arc):
        return False
    return self.id == other.id

  def __hash__(self):
      return hash(self.id)
