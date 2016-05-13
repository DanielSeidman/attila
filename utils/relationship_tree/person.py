class Person:
  def __init__(self, fid, iid, father_id, mother_id, sex, birthday, datapresent):
    self.fid = fid
    self.iid = iid
    self.father_id = father_id
    self.mother_id = mother_id
    self.sex = sex
    self.birthday = birthday
    self.datapresent = datapresent

    self.father = None
    self.mother = None
    self.children = []

  def set_father(self, father):
    if isinstance(father, Person):
      self.father = father

  def set_mother(self, mother):
    if isinstance(mother, Person):
      self.mother = mother

  def add_child(self, child):
    if isinstance(child, Person) and child not in self.children:
      self.children.append(child)

  def get_parents(self):
    parents = []

    if self.father:
      parents.append(self.father)
    if self.mother:
      parents.append(self.mother)

    return parents

  '''
  Method for determining relationship:
  (1) Find your nearest common ancestor. For this version, there is assumed
  to only be one. With more complex populations, this will need to be relaxed.

  (2) Compare the distance of each person to that common ancestor according to
  http://www.searchforancestors.com/utility/cousincalculator.html
  '''

  def relationship_to(self, person):
    # Return the relationship between self and person.
    # The form is 'self is X of person'
    # 'self is child of person'
    # 'self is parent of person'
    relationship = None
    nca = self.nearest_common_ancestor(person)

    if nca:
      relationship = _relationship(self.distance_to_ancestor(nca), person.distance_to_ancestor(nca))
      if relationship == 'sibling' and self.get_parents() != person.get_parents():
        relationship = 'half-sibling'

    return relationship

  def meiotic_distance(self, person):
    nca = self.nearest_common_ancestor(person)

    if nca is not None:
      return self.distance_to_ancestor(nca) + person.distance_to_ancestor(nca)
    else:
      return None

  def nearest_common_ancestor(self, person):
    common_ancestor = None

    checked = set()
    not_checked = [self, person]

    while not_checked and not common_ancestor:
      candidate = not_checked.pop(0)
      if candidate in checked:
        common_ancestor = candidate
      else:
        checked.add(candidate)
        not_checked += candidate.get_parents()

    return common_ancestor

  def distance_to_ancestor(self, ancestor):
    # Find the distance by BFS.
    not_checked = [(self, 0)]

    while not_checked:
      candidate, distance = not_checked.pop(0)
      if candidate is ancestor:
        return distance
      else:
        for parent in candidate.get_parents():
          not_checked.append((parent, distance + 1))

    return None


# def _relationship(distance_a, distance_b):
#   # This version has reciprocal relationships put into the same bucket.

#   #############################
#   # One of the two is the NCA #
#   #############################

#   if distance_a == 0 and distance_b == 0:
#     return 'self'

#   elif distance_a == 0 or distance_b == 0:
#     if distance_a == 1 or distance_b == 1:
#       return 'parent//child'
#     else:
#       if distance_a == 0:
#         return ((distance_b-2)*'great')+'grand(parent//child)'
#       else: # distance_b == 0
#         return ((distance_a-2)*'great')+'grand(parent//child)'

#   ######################
#   # Neither is the NCA #
#   ######################

#   elif distance_a == 1 and distance_b == 1: # Siblings
#     return 'sibling'

#   elif distance_a == 1 or distance_b == 1: # Niece/nephew of b
#     if distance_a == 2 or distance_b == 2:
#       return 'aunt/uncle//niece/nephew'
#     else:
#       if distance_a == 1:
#         return ((distance_b-2)*'great')+'grand(aunt/uncle//niece/nephew)'
#       else:
#         return ((distance_a-2)*'great')+'grand(aunt/uncle//niece/nephew)'

#   else: # Cousin relationship
#     return str(min(distance_a-1, distance_b-1))+ \
#            _suffix(min(distance_a-1, distance_b-1)) + \
#            '-cousin-' + \
#            str(abs(distance_a - distance_b))+'-times-removed'


# This code is tested as working.
def _relationship(distance_a, distance_b):
  # Return the relationship between a and b given
  # the distance of a and b to their nearest common
  # ancestor.
  # Relationships are in terms of A's perspective.
  # A is sibling of B.
  # A is aunt/uncle of B.

  if distance_a == 0 and distance_b == 0:
    return 'self'

  elif distance_a == 0: # X Parent relationship
    if distance_b == 1:
      return 'parent'
    else:
      return ((distance_b-2)*'great')+'grandparent'

  elif distance_b == 0: # X Child relationship
    if distance_a == 1:
      return 'child'
    else:
      return ((distance_a-2)*'great')+'grandchild'

  elif distance_a - distance_b == 0 and distance_a == 1: # Siblings
    return 'sibling'

  elif distance_a == 1: # Niece/nephew of b
    if distance_b == 2:
      return 'niece/nephew'
    else:
      return ((distance_b-2)*'great')+'grandniece/nephew'

  elif distance_b == 1: # Aunt/uncle of b
    if distance_a == 2:
      return 'aunt/uncle'
    else:
      return ((distance_a-2)*'great')+'grandaunt/uncle'

  else: # Cousin relationship
    return str(min(distance_a-1, distance_b-1))+ \
           _suffix(min(distance_a-1, distance_b-1)) + \
           '-cousin-' + \
           str(abs(distance_a - distance_b))+'-times-removed'

# Above directed relationship code updated to use sex information
# def _relationship(distance_a, distance_b, sex_of_a):
#   # Return the relationship between a and b given
#   # the distance of a and b to their nearest common
#   # ancestor.
#   # Relationships are in terms of A's perspective.
#   # A is sibling of B.
#   # A is aunt/uncle of B.

#   NIECE_NEPHEW = {'M': 'nephew', 'F': 'niece'}
#   AUNT_UNCLE = {'M': 'uncle', 'F': 'aunt'}

#   if distance_a == 0 and distance_b == 0:
#     return 'self'

#   elif distance_a == 0: # X Parent relationship
#     if distance_b == 1:
#       return 'parent'
#     else:
#       return ((distance_b-2)*'great')+'grandparent'

#   elif distance_b == 0: # X Child relationship
#     if distance_a == 1:
#       return 'child'
#     else:
#       return ((distance_a-2)*'great')+'grandchild'

#   elif distance_a - distance_b == 0 and distance_a == 1: # Siblings
#     return 'sibling'

#   elif distance_a == 1: # Niece/nephew of b
#     if distance_b == 2:
#       return NIECE_NEPHEW[sex_of_a]
#     else:
#       return ((distance_b-2)*'great')+'grand'+NIECE_NEPHEW[sex_of_a]

#   elif distance_b == 1: # Aunt/uncle of b
#     if distance_a == 2:
#       return AUNT_UNCLE[sex_of_a]
#     else:
#       return ((distance_a-2)*'great')+'grand'+AUNT_UNCLE[sex_of_a]

#   else: # Cousin relationship
#     return str(min(distance_a-1, distance_b-1))+ \
#            _suffix(min(distance_a-1, distance_b-1)) + \
#            '-cousin-' + \
#            str(abs(distance_a - distance_b))+'-times-removed'


def _suffix(num):
  if num == 1:
    return 'st'
  elif num == 2:
    return 'nd'
  elif num == 3:
    return 'rd'
  else:
    return 'th'
