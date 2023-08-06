import snakes.plugins
snakes.plugins.load("gv", "snakes.nets", "nets")
from nets import *

class SNAKES:
  def __init__(self, resource):
    self.resource = resource
    self.places = resource.places()
    self.trans = resource.transitions()
    self.arcs = resource.arcs()

  def convert(self):
    n = PetriNet("snakes")
    ptot, ttop = [], []

    for place_id, place in self.places.items():
      if place['initmark']:
        p = Place(place['text'], self.resource._token(place['initmark']))
      else:
        p = Place(place['text'])

      n.add_place(p)

    for trnas_id, transition in self.trans.items():
      time = transition['time'].replace('@+','')
      t = Transition(transition['text'], Expression(str(time or 0)))
      n.add_transition(t)

    for arc in self.arcs.values():
      placeend = arc['placeend']
      transend = arc['transend']
      if arc['orientation'] == 'PtoT':
        n.add_input(self.places[placeend]['text'], self.trans[transend]['text'], Value(0))

      elif arc['orientation'] == 'TtoP':
        n.add_output(self.places[placeend]['text'], self.trans[transend]['text'], Value(0))
      
      elif arc['orientation'] == 'BOTHDIR':
        n.add_input(self.places[placeend]['text'], self.trans[transend]['text'], Value(0))
        n.add_output(self.places[placeend]['text'], self.trans[transend]['text'], Value(0))

    # n.draw('../data/models/snakes/fsp.png')
    return n 

  # def _token(self, tokens):
  #   tokens = tokens.replace('\n','').split('++')
  #   token_list = []
  #   for token in tokens:
  #     token_num = int(token.split('`')[0])
  #     token_list += [ token.split('`')[1] for i in range(token_num) ]

  #   return token_list

class SnakesFromPm4py:
  def __init__(self, net):
    self.places = net.places
    self.transitions = net.transitions
    self.arcs = net.arcs

  def replace_symbol(self, arc):
    """
    arc: string
    ex) arc = '(p)({'examine thoroughly', 'examine casually'}, {'decide'})->(t)decide'
    This function remove (p) or (t) symbol from net.arcs
    """
    if '(p)' in arc:
      return arc.replace('(p)',"")
    elif '(t)' in arc:
      return arc.replace('(t)',"")
  
  def set_arc(self):
    arcs = dict()
    for arc in self.arcs:
      arc_list = self.replace_symbol(str(arc))
      arcs[arc_list[0]] = arc_list[1]


  def convert(self):
    n = PetriNet('snakes')
    for place in self.places:
      p = Place(str(place))
      n.add_place(p)
    
    for trans in self.transitions:
      t = Transition(str(trans))
      n.add_transition(t)

    for arc in self.arcs:
      conn = str(arc).split('->')
      if '(p)' in conn[0]:
        n.add_input(self.replace_symbol(conn[0]), self.replace_symbol(conn[1]), Value(0))
      else:
        n.add_output(self.replace_symbol(conn[1]), self.replace_symbol(conn[0]), Value(0))

    return n
  
  