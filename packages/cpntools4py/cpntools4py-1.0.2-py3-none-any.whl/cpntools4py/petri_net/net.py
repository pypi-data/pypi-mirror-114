from .obj.place import Place
from .obj.transition import Transition
from .obj.arc import Arc

class CPN:
  def __init__(self, xml_doc):
    self.__doc = xml_doc

  @property
  def places(self):
    places = []
    for place_doc in self.__doc.findall('place'):
      place = Place(place_doc)
      places.append(place)

    return places

  @property
  def transitions(self):
    transitions = []
    for trans_doc in self.__doc.findall('trans'):
      trans = Transition(trans_doc)
      transitions.append(trans)

    return transitions
  
  @property
  def arcs(self):
    arcs = []
    for arc_doc in self.__doc.findall('arc'):
      arc = Arc(arc_doc)
      arcs.append(arc)
    
    return arcs

  def fetch(self, id):
    nodes = self.places + self.transitions
    for node in nodes:
      if not node.id == id:
        continue

      return node
