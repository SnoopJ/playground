"""
  mcspud introduced me to the idea of Lenses ("functional references") for
  manipulating highly structured data, so this is all his fault
"""
from pprint import pprint
from lenses import lens
import json

with open('spells.json', 'r') as f:
  data = json.load(f)

def munge_level(lvl):
  """
  Turn obnoxious data like 'level': 'wizard/sorceror 2, bard 3' into
  'level': {'wizard': 2, 'sorceror': 2, 'bard': 3}
  """
  lvls = {}
  for spec in lvl.split(','):
    if len(spec) < 0:
      continue
    cls, lvl = spec.split()
    if '/' in cls:
      cls = cls.split('/')
    else:
      cls = [cls]
    for c in cls:
      lvls[c] = int(lvl)
  return lvls

def spellfold(spell):
  lvls = munge_level(spell['level'])
  yield {'name': spell['name'],
         'level': lvls}


spellfields = lens.Each()['fields']  # focus the fields of a spell

cls = 'wizard'
clsfilter = lens.Filter(lambda s: cls in s['level'])  # filter spells in this class

mutatespell = lens.Fold(spellfold)  # use a fold to mutate the spell structure

optic = (spellfields & clsfilter & mutatespell)  # compose these lenses
spells = optic.collect()(data)
print('\n----\nFirst 10 %s spells:\n----' % cls)
pprint([s['name'] for s in spells[:10]])
pprint(spells[:10])

# I changed my mind and want to see spells with mixed class levels
optic = optic & lens.Filter(lambda s: len(set(s['level'].values())) > 1)
spells = optic.collect()(data)
print('\n----\nFirst 10 %s spells with level variation:\n----' % cls)
pprint([s['name'] for s in spells[:10]])
pprint(spells[:10])
